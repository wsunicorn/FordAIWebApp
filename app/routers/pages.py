from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, Response
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.templates import common_context, templates
from app.data.site_content import (
    ON_ROAD_ASSUMPTIONS,
    PRICE_SOURCE_URL,
    PUBLIC_ROUTES,
    SOURCE_CHECKED_AT,
    SOURCE_PERIOD,
    VEHICLES,
    format_vnd,
)
from app.db.session import get_session
from app.schemas import LeadCreate
from app.services.i18n_service import (
    localize_vehicles,
    localized_url,
    request_locale,
    t,
)
from app.services.lead_service import create_lead
from app.services.public_content_service import (
    public_faqs,
    public_promotions,
    public_vehicle,
    public_vehicle_options,
    public_vehicles,
)

router = APIRouter(tags=["pages"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


def page_context(request: Request, **extra: object) -> dict[str, object]:
    locale = request_locale(request)

    def translate(key: str, **kwargs: object) -> str:
        return t(locale, key, **kwargs)

    def lang_path(path: str, target_locale: str | None = None) -> str:
        return localized_url(
            path,
            target_locale or locale,
            request.url.query,
        )

    canonical_suffix = request.url.path
    if locale != "vi":
        canonical_suffix = localized_url(request.url.path, locale)

    return {
        **common_context(),
        "request": request,
        "locale": locale,
        "t": translate,
        "lang_path": lang_path,
        "lang_switch_url": lambda target_locale: localized_url(
            request.url.path,
            target_locale,
            request.url.query,
        ),
        "current_path": request.url.path,
        "canonical_url": f"{str(settings.app_url).rstrip('/')}{canonical_suffix}",
        "vehicles": VEHICLES,
        "vehicle_options": public_vehicle_options(VEHICLES),
        "format_vnd": format_vnd,
        "source_period": SOURCE_PERIOD,
        "source_checked_at": SOURCE_CHECKED_AT,
        "price_source_url": PRICE_SOURCE_URL,
        **extra,
    }


async def public_page_context(
    request: Request,
    session: AsyncSession,
    **extra: object,
) -> dict[str, object]:
    locale = request_locale(request)
    vehicles = localize_vehicles(await public_vehicles(session), locale)
    return page_context(
        request,
        vehicles=vehicles,
        vehicle_options=public_vehicle_options(vehicles),
        **extra,
    )


def selected_vehicle_name(request: Request, vehicles: object) -> str:
    selected = request.query_params.get("vehicle")
    if not selected:
        return ""
    return next(
        (
            vehicle.name
            for vehicle in vehicles
            if vehicle.slug == selected or vehicle.name == selected
        ),
        "",
    )


def safe_success_redirect(path: str) -> str:
    redirect_path = path if path.startswith("/") and not path.startswith("//") else "/"
    separator = "&" if "?" in redirect_path else "?"
    return f"{redirect_path}{separator}{urlencode({'lead': 'success'})}"


@router.head("/")
async def home_head() -> Response:
    return Response(status_code=200)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: SessionDep):
    locale = request_locale(request)
    vehicles = localize_vehicles(await public_vehicles(session), locale)
    promotions = await public_promotions(session)
    faqs = await public_faqs(session)
    return templates.TemplateResponse(
        request,
        "pages/home.html",
        page_context(
            request,
            vehicles=vehicles,
            vehicle_options=public_vehicle_options(vehicles),
            page_title=t(locale, "meta.home.title"),
            page_description=t(locale, "meta.home.description"),
            featured_vehicles=vehicles[:4],
            promotions=promotions,
            faqs=faqs[:3],
        ),
    )


@router.get("/anh-huy", response_class=HTMLResponse)
async def about_huy(request: Request, session: SessionDep):
    return templates.TemplateResponse(
        request,
        "pages/about.html",
        await public_page_context(
            request,
            session,
            page_title="Anh Huỳnh Đang Huy - Tư vấn bán hàng Ford",
            page_description=(
                "Thông tin liên hệ, vai trò và cách anh Huy hỗ trợ "
                "khách hàng Ford tại Đồng Tháp."
            ),
        ),
    )


@router.get("/xe", response_class=HTMLResponse)
async def vehicles(request: Request, session: SessionDep):
    locale = request_locale(request)
    return templates.TemplateResponse(
        request,
        "pages/vehicles.html",
        await public_page_context(
            request,
            session,
            page_title=t(locale, "meta.vehicles.title"),
            page_description=t(locale, "meta.vehicles.description"),
        ),
    )


@router.get("/xe/{slug}", response_class=HTMLResponse)
async def vehicle_detail(request: Request, slug: str, session: SessionDep):
    locale = request_locale(request)
    raw_vehicle = await public_vehicle(session, slug)
    vehicle = localize_vehicles((raw_vehicle,), locale)[0] if raw_vehicle else None
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return templates.TemplateResponse(
        request,
        "pages/vehicle_detail.html",
        await public_page_context(
            request,
            session,
            vehicle=vehicle,
            page_title=f"{vehicle.name} - Giá tham khảo và tư vấn",
            page_description=(
                f"Thông tin {vehicle.name}, phiên bản, giá tham khảo "
                "và form liên hệ anh Huy."
            ),
        ),
    )


@router.get("/so-sanh", response_class=HTMLResponse)
async def compare(request: Request, session: SessionDep):
    return templates.TemplateResponse(
        request,
        "pages/compare.html",
        await public_page_context(
            request,
            session,
            page_title="So sánh nhanh xe Ford",
            page_description="So sánh nhanh các dòng xe Ford theo giá, nhóm xe và nhu cầu sử dụng.",
        ),
    )


@router.get("/bang-gia", response_class=HTMLResponse)
async def price_table(request: Request, session: SessionDep):
    locale = request_locale(request)
    return templates.TemplateResponse(
        request,
        "pages/prices.html",
        await public_page_context(
            request,
            session,
            page_title=t(locale, "meta.prices.title"),
            page_description=t(locale, "meta.prices.description"),
        ),
    )


@router.get("/du-toan-lan-banh", response_class=HTMLResponse)
async def on_road_calculator(request: Request, session: SessionDep):
    return templates.TemplateResponse(
        request,
        "pages/on_road.html",
        await public_page_context(
            request,
            session,
            page_title="Dự toán chi phí lăn bánh Ford",
            page_description="Ước tính chi phí lăn bánh tham khảo và gửi phương án cho anh Huy.",
            assumptions=ON_ROAD_ASSUMPTIONS,
        ),
    )


@router.get("/du-toan-tra-gop", response_class=HTMLResponse)
async def loan_calculator(request: Request, session: SessionDep):
    return templates.TemplateResponse(
        request,
        "pages/loan.html",
        await public_page_context(
            request,
            session,
            page_title="Dự toán trả góp xe Ford",
            page_description="Ước tính trả góp xe Ford, không phải cam kết duyệt vay.",
        ),
    )


@router.get("/uu-dai", response_class=HTMLResponse)
async def promotions(request: Request, session: SessionDep):
    promotions = await public_promotions(session)
    return templates.TemplateResponse(
        request,
        "pages/promotions.html",
        await public_page_context(
            request,
            session,
            page_title="Ưu đãi Ford cần xác nhận",
            page_description="Xem các nhóm ưu đãi tham khảo và gửi yêu cầu để anh Huy xác nhận.",
            promotions=promotions,
        ),
    )


@router.get("/faq", response_class=HTMLResponse)
async def faq(request: Request, session: SessionDep):
    faqs = await public_faqs(session)
    return templates.TemplateResponse(
        request,
        "pages/faq.html",
        await public_page_context(
            request,
            session,
            page_title="Câu hỏi thường gặp khi mua xe Ford",
            page_description="FAQ về giá, lăn bánh, trả góp, lái thử và liên hệ anh Huy.",
            faqs=faqs,
        ),
    )


@router.get("/tro-ly-ai", response_class=HTMLResponse)
async def ai_assistant(request: Request, session: SessionDep):
    return templates.TemplateResponse(
        request,
        "pages/ai_assistant.html",
        await public_page_context(
            request,
            session,
            page_title="Trợ lý AI tư vấn Ford",
            page_description=(
                "Hỏi AI về xe Ford, giá tham khảo, lăn bánh, trả góp và chuyển yêu cầu "
                "cho anh Huy khi cần xác nhận trực tiếp."
            ),
        ),
    )


@router.get("/lien-he", response_class=HTMLResponse)
async def contact(request: Request, session: SessionDep):
    return templates.TemplateResponse(
        request,
        "pages/contact.html",
        await public_page_context(
            request,
            session,
            page_title="Liên hệ anh Huy Ford Đồng Tháp",
            page_description="Gọi, Zalo, email, Facebook hoặc gửi form để anh Huy liên hệ lại.",
        ),
    )


@router.get("/lai-thu", response_class=HTMLResponse)
async def test_drive(request: Request, session: SessionDep):
    locale = request_locale(request)
    vehicles = localize_vehicles(await public_vehicles(session), locale)
    return templates.TemplateResponse(
        request,
        "pages/test_drive.html",
        page_context(
            request,
            vehicles=vehicles,
            vehicle_options=public_vehicle_options(vehicles),
            selected_vehicle=selected_vehicle_name(request, vehicles),
            page_title="Đăng ký lái thử Ford",
            page_description=(
                "Để lại thông tin xe, khu vực và thời gian mong muốn "
                "để anh Huy xác nhận lịch."
            ),
        ),
    )


@router.get("/bao-gia", response_class=HTMLResponse)
async def quote(request: Request, session: SessionDep):
    locale = request_locale(request)
    vehicles = localize_vehicles(await public_vehicles(session), locale)
    return templates.TemplateResponse(
        request,
        "pages/quote.html",
        page_context(
            request,
            vehicles=vehicles,
            vehicle_options=public_vehicle_options(vehicles),
            selected_vehicle=selected_vehicle_name(request, vehicles),
            page_title=t(locale, "meta.quote.title"),
            page_description=t(locale, "meta.quote.description"),
        ),
    )


@router.post("/lead")
async def submit_lead(
    session: SessionDep,
    full_name: str = Form(...),
    phone: str = Form(...),
    vehicle_interest: str | None = Form(default=None),
    area: str | None = Form(default=None),
    need_type: str = Form(default="quote"),
    note: str | None = Form(default=None),
    redirect_to: str = Form(default="/"),
):
    try:
        lead_in = LeadCreate(
            full_name=full_name,
            phone=phone,
            vehicle_interest=vehicle_interest,
            area=area,
            need_type=need_type,
            note=note,
        )
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    await create_lead(session, lead_in)

    return RedirectResponse(url=safe_success_redirect(redirect_to), status_code=303)


@router.get("/robots.txt")
async def robots_txt() -> Response:
    body = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin",
            "Disallow: /api",
            f"Sitemap: {str(settings.app_url).rstrip('/')}/sitemap.xml",
        ]
    )
    return Response(content=body, media_type="text/plain")


@router.get("/favicon.ico", include_in_schema=False)
async def favicon_ico() -> FileResponse:
    return FileResponse("assets/brand/favicon.svg", media_type="image/svg+xml")


@router.get("/sitemap.xml")
async def sitemap_xml() -> Response:
    base_url = str(settings.app_url).rstrip("/")
    url_items = "\n".join(
        f"""  <url>
    <loc>{base_url}{route}</loc>
    <lastmod>{SOURCE_CHECKED_AT}</lastmod>
    <changefreq>{"daily" if route == "/" else "weekly"}</changefreq>
    <priority>{"1.0" if route == "/" else "0.7"}</priority>
  </url>"""
        for route in PUBLIC_ROUTES
    )
    body = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{url_items}
</urlset>
"""
    return Response(content=body, media_type="application/xml")
