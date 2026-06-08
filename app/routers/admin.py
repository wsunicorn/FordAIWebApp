from __future__ import annotations

import csv
from io import StringIO
from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin_auth import (
    ADMIN_SESSION_COOKIE,
    create_admin_session,
    require_admin,
    verify_admin_credentials,
)
from app.core.config import settings
from app.core.templates import common_context, templates
from app.db.session import get_session
from app.models import ContentItem, VehiclePrice, VehicleVariant
from app.services.admin_service import (
    APPROVAL_STATUSES,
    CONTENT_KINDS,
    FRESHNESS_STATUSES,
    LEAD_STATUSES,
    content_freshness_counts,
    create_content_item,
    get_lead_or_none,
    get_vehicle_or_none,
    lead_status_counts,
    list_content_items,
    list_leads,
    list_vehicles,
    parse_optional_date,
    parse_optional_datetime,
    recent_audit_logs,
    seed_content_from_source,
    seed_vehicles_from_source,
    update_content_item,
    update_lead_care,
    update_price,
    update_variant,
    update_vehicle,
)
from app.services.ai_service import (
    ai_dashboard_stats,
    list_ai_documents,
    recent_ai_conversations,
    seed_ai_documents,
)

router = APIRouter(tags=["admin"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]
AdminDep = Annotated[str, Depends(require_admin)]


def admin_context(
    request: Request,
    admin_user: str | None = None,
    **extra: object,
) -> dict[str, object]:
    return {
        **common_context(),
        "request": request,
        "current_path": request.url.path,
        "admin_user": admin_user,
        "lead_statuses": LEAD_STATUSES,
        "content_kinds": CONTENT_KINDS,
        "approval_statuses": APPROVAL_STATUSES,
        "freshness_statuses": FRESHNESS_STATUSES,
        **extra,
    }


def admin_redirect(path: str, message: str | None = None) -> RedirectResponse:
    separator = "&" if "?" in path else "?"
    url = f"{path}{separator}{urlencode({'message': message})}" if message else path
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


def validate_choice(value: str, allowed: tuple[str, ...], field_name: str) -> str:
    if value not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid {field_name}")
    return value


@router.get("/admin/login", response_class=HTMLResponse)
async def admin_login(request: Request, next: str = "/admin", error: str | None = None):
    return templates.TemplateResponse(
        request,
        "admin/login.html",
        admin_context(
            request,
            page_title="Admin login",
            next_path=next,
            error=error or request.query_params.get("message"),
        ),
    )


@router.post("/admin/login")
async def admin_login_submit(
    username: str = Form(...),
    password: str = Form(...),
    next_path: str = Form(default="/admin"),
):
    if not verify_admin_credentials(username, password):
        return admin_redirect("/admin/login", "Sai tai khoan hoac mat khau")

    target = next_path if next_path.startswith("/") and not next_path.startswith("//") else "/admin"
    response = RedirectResponse(url=target, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        ADMIN_SESSION_COOKIE,
        create_admin_session(username),
        max_age=settings.admin_session_ttl_seconds,
        httponly=True,
        secure=settings.app_env == "production",
        samesite="lax",
    )
    return response


@router.post("/admin/logout")
async def admin_logout():
    response = RedirectResponse(url="/admin/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(ADMIN_SESSION_COOKIE)
    return response


@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, session: SessionDep, admin_user: AdminDep):
    lead_counts = await lead_status_counts(session)
    freshness_counts = await content_freshness_counts(session)
    recent_leads = await list_leads(session, limit=8)
    audit_logs = await recent_audit_logs(session, limit=10)

    return templates.TemplateResponse(
        request,
        "admin/dashboard.html",
        admin_context(
            request,
            admin_user,
            page_title="Admin dashboard",
            lead_counts=lead_counts,
            freshness_counts=freshness_counts,
            recent_leads=recent_leads,
            audit_logs=audit_logs,
        ),
    )


@router.get("/admin/leads", response_class=HTMLResponse)
async def admin_leads(
    request: Request,
    session: SessionDep,
    admin_user: AdminDep,
    status_filter: str | None = None,
    q: str | None = None,
):
    leads = await list_leads(session, status=status_filter, query=q)
    counts = await lead_status_counts(session)
    return templates.TemplateResponse(
        request,
        "admin/leads.html",
        admin_context(
            request,
            admin_user,
            page_title="Lead inbox",
            leads=leads,
            counts=counts,
            status_filter=status_filter,
            q=q or "",
        ),
    )


@router.get("/admin/leads/export.csv")
async def admin_leads_export(
    session: SessionDep,
    _: AdminDep,
    status_filter: str | None = None,
    q: str | None = None,
):
    leads = await list_leads(session, status=status_filter, query=q, limit=10_000)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "id",
            "created_at",
            "full_name",
            "phone",
            "vehicle_interest",
            "area",
            "need_type",
            "status",
            "follow_up_at",
            "last_contacted_at",
            "note",
            "admin_note",
        ]
    )
    for lead in leads:
        writer.writerow(
            [
                lead.id,
                lead.created_at.isoformat(),
                lead.full_name,
                lead.phone,
                lead.vehicle_interest or "",
                lead.area or "",
                lead.need_type,
                lead.status,
                lead.follow_up_at.isoformat() if lead.follow_up_at else "",
                lead.last_contacted_at.isoformat() if lead.last_contacted_at else "",
                lead.note or "",
                lead.admin_note or "",
            ]
        )

    return Response(
        content=output.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="leads.csv"'},
    )


@router.get("/admin/leads/{lead_id}", response_class=HTMLResponse)
async def admin_lead_detail(
    request: Request,
    lead_id: str,
    session: SessionDep,
    admin_user: AdminDep,
):
    lead = await get_lead_or_none(session, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    audit_logs = await recent_audit_logs(session, limit=25)
    related_logs = [log for log in audit_logs if log.entity_id == lead.id]
    return templates.TemplateResponse(
        request,
        "admin/lead_detail.html",
        admin_context(
            request,
            admin_user,
            page_title=f"Lead {lead.full_name}",
            lead=lead,
            related_logs=related_logs,
        ),
    )


@router.post("/admin/leads/{lead_id}")
async def admin_lead_update(
    lead_id: str,
    session: SessionDep,
    _: AdminDep,
    lead_status: str = Form(...),
    admin_note: str | None = Form(default=None),
    follow_up_at: str | None = Form(default=None),
    last_contacted_at: str | None = Form(default=None),
):
    lead = await get_lead_or_none(session, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    await update_lead_care(
        session,
        lead,
        status=validate_choice(lead_status, LEAD_STATUSES, "lead status"),
        admin_note=admin_note,
        follow_up_at=parse_optional_datetime(follow_up_at),
        last_contacted_at=parse_optional_datetime(last_contacted_at),
    )
    return admin_redirect(f"/admin/leads/{lead.id}", "Da cap nhat lead")


@router.get("/admin/vehicles", response_class=HTMLResponse)
async def admin_vehicles(request: Request, session: SessionDep, admin_user: AdminDep):
    vehicles = await list_vehicles(session)
    return templates.TemplateResponse(
        request,
        "admin/vehicles.html",
        admin_context(
            request,
            admin_user,
            page_title="Quan ly xe va gia",
            vehicles=vehicles,
        ),
    )


@router.post("/admin/vehicles/seed")
async def admin_vehicles_seed(session: SessionDep, _: AdminDep):
    count = await seed_vehicles_from_source(session)
    return admin_redirect("/admin/vehicles", f"Da seed {count} dong xe")


@router.get("/admin/vehicles/{vehicle_id}", response_class=HTMLResponse)
async def admin_vehicle_detail(
    request: Request,
    vehicle_id: str,
    session: SessionDep,
    admin_user: AdminDep,
):
    vehicle = await get_vehicle_or_none(session, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return templates.TemplateResponse(
        request,
        "admin/vehicle_detail.html",
        admin_context(
            request,
            admin_user,
            page_title=f"Quan ly {vehicle.name}",
            vehicle=vehicle,
        ),
    )


@router.post("/admin/vehicles/{vehicle_id}")
async def admin_vehicle_update(
    vehicle_id: str,
    session: SessionDep,
    _: AdminDep,
    name: str = Form(...),
    category: str = Form(...),
    summary: str | None = Form(default=None),
    source_url: str | None = Form(default=None),
    source_updated_at: str | None = Form(default=None),
    review_due_at: str | None = Form(default=None),
    approval_status: str = Form(...),
    freshness_status: str = Form(...),
):
    vehicle = await get_vehicle_or_none(session, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    await update_vehicle(
        session,
        vehicle,
        name=name,
        category=category,
        summary=summary,
        source_url=source_url,
        source_updated_at=parse_optional_date(source_updated_at),
        review_due_at=parse_optional_date(review_due_at),
        approval_status=validate_choice(approval_status, APPROVAL_STATUSES, "approval status"),
        freshness_status=validate_choice(freshness_status, FRESHNESS_STATUSES, "freshness status"),
    )
    return admin_redirect(f"/admin/vehicles/{vehicle.id}", "Da cap nhat xe")


@router.post("/admin/vehicles/{vehicle_id}/variants/{variant_id}")
async def admin_variant_update(
    vehicle_id: str,
    variant_id: str,
    session: SessionDep,
    _: AdminDep,
    name: str = Form(...),
    engine: str | None = Form(default=None),
    sort_order: int = Form(default=0),
):
    variant = await session.get(VehicleVariant, variant_id)
    if not variant or variant.vehicle_id != vehicle_id:
        raise HTTPException(status_code=404, detail="Variant not found")

    await update_variant(session, variant, name=name, engine=engine, sort_order=sort_order)
    return admin_redirect(f"/admin/vehicles/{vehicle_id}", "Da cap nhat phien ban")


@router.post("/admin/vehicles/{vehicle_id}/prices/{price_id}")
async def admin_price_update(
    vehicle_id: str,
    price_id: str,
    session: SessionDep,
    _: AdminDep,
    price_vnd: int = Form(...),
    source_url: str | None = Form(default=None),
    source_updated_at: str | None = Form(default=None),
    effective_to: str | None = Form(default=None),
    review_due_at: str | None = Form(default=None),
    freshness_status: str = Form(...),
):
    price = await session.get(VehiclePrice, price_id)
    if not price or price.vehicle_id != vehicle_id:
        raise HTTPException(status_code=404, detail="Price not found")

    await update_price(
        session,
        price,
        price_vnd=price_vnd,
        source_url=source_url,
        source_updated_at=parse_optional_date(source_updated_at),
        effective_to=parse_optional_date(effective_to),
        review_due_at=parse_optional_date(review_due_at),
        freshness_status=validate_choice(freshness_status, FRESHNESS_STATUSES, "freshness status"),
    )
    return admin_redirect(f"/admin/vehicles/{vehicle_id}", "Da cap nhat gia")


@router.get("/admin/content", response_class=HTMLResponse)
async def admin_content(
    request: Request,
    session: SessionDep,
    admin_user: AdminDep,
    kind: str | None = None,
):
    items = await list_content_items(session, kind=kind)
    return templates.TemplateResponse(
        request,
        "admin/content.html",
        admin_context(
            request,
            admin_user,
            page_title="Quan ly noi dung",
            items=items,
            kind_filter=kind or "",
        ),
    )


@router.get("/admin/ai", response_class=HTMLResponse)
async def admin_ai(request: Request, session: SessionDep, admin_user: AdminDep):
    stats = await ai_dashboard_stats(session)
    documents = await list_ai_documents(session)
    conversations = await recent_ai_conversations(session)
    return templates.TemplateResponse(
        request,
        "admin/ai.html",
        admin_context(
            request,
            admin_user,
            page_title="AI assistant",
            stats=stats,
            documents=documents,
            conversations=conversations,
        ),
    )


@router.post("/admin/ai/seed")
async def admin_ai_seed(session: SessionDep, _: AdminDep):
    count = await seed_ai_documents(session)
    return admin_redirect("/admin/ai", f"Da seed {count} tai lieu AI")


@router.post("/admin/content/seed")
async def admin_content_seed(session: SessionDep, _: AdminDep):
    count = await seed_content_from_source(session)
    return admin_redirect("/admin/content", f"Da seed {count} noi dung")


@router.post("/admin/content")
async def admin_content_create(
    session: SessionDep,
    _: AdminDep,
    kind: str = Form(...),
    title: str = Form(...),
    body: str | None = Form(default=None),
    source_url: str | None = Form(default=None),
    source_updated_at: str | None = Form(default=None),
    effective_to: str | None = Form(default=None),
    review_due_at: str | None = Form(default=None),
    approval_status: str = Form(...),
    freshness_status: str = Form(...),
):
    await create_content_item(
        session,
        kind=validate_choice(kind, CONTENT_KINDS, "content kind"),
        title=title,
        body=body,
        source_url=source_url,
        source_updated_at=parse_optional_date(source_updated_at),
        effective_to=parse_optional_date(effective_to),
        review_due_at=parse_optional_date(review_due_at),
        approval_status=validate_choice(approval_status, APPROVAL_STATUSES, "approval status"),
        freshness_status=validate_choice(freshness_status, FRESHNESS_STATUSES, "freshness status"),
    )
    return admin_redirect("/admin/content", "Da tao noi dung")


@router.post("/admin/content/{content_id}")
async def admin_content_update(
    content_id: str,
    session: SessionDep,
    _: AdminDep,
    kind: str = Form(...),
    title: str = Form(...),
    body: str | None = Form(default=None),
    source_url: str | None = Form(default=None),
    source_updated_at: str | None = Form(default=None),
    effective_to: str | None = Form(default=None),
    review_due_at: str | None = Form(default=None),
    approval_status: str = Form(...),
    freshness_status: str = Form(...),
):
    content_item = await session.get(ContentItem, content_id)
    if not content_item:
        raise HTTPException(status_code=404, detail="Content item not found")

    await update_content_item(
        session,
        content_item,
        kind=validate_choice(kind, CONTENT_KINDS, "content kind"),
        title=title,
        body=body,
        source_url=source_url,
        source_updated_at=parse_optional_date(source_updated_at),
        effective_to=parse_optional_date(effective_to),
        review_due_at=parse_optional_date(review_due_at),
        approval_status=validate_choice(approval_status, APPROVAL_STATUSES, "approval status"),
        freshness_status=validate_choice(freshness_status, FRESHNESS_STATUSES, "freshness status"),
    )
    return admin_redirect("/admin/content", "Da cap nhat noi dung")
