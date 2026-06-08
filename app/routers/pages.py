from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, Response
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.templates import common_context, templates
from app.data.site_content import (
    FAQS,
    ON_ROAD_ASSUMPTIONS,
    PRICE_SOURCE_URL,
    PROMOTIONS,
    PUBLIC_ROUTES,
    SOURCE_CHECKED_AT,
    SOURCE_PERIOD,
    VEHICLES,
    format_vnd,
    get_vehicle,
    vehicle_options,
)
from app.db.session import get_session
from app.schemas import LeadCreate
from app.services.lead_service import create_lead

router = APIRouter(tags=["pages"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


def page_context(request: Request, **extra: object) -> dict[str, object]:
    return {
        **common_context(),
        "request": request,
        "current_path": request.url.path,
        "vehicles": VEHICLES,
        "vehicle_options": vehicle_options(),
        "format_vnd": format_vnd,
        "source_period": SOURCE_PERIOD,
        "source_checked_at": SOURCE_CHECKED_AT,
        "price_source_url": PRICE_SOURCE_URL,
        **extra,
    }


def safe_success_redirect(path: str) -> str:
    redirect_path = path if path.startswith("/") and not path.startswith("//") else "/"
    separator = "&" if "?" in redirect_path else "?"
    return f"{redirect_path}{separator}{urlencode({'lead': 'success'})}"


@router.head("/")
async def home_head() -> Response:
    return Response(status_code=200)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/home.html",
        page_context(
            request,
            page_title="Huỳnh Đang Huy - Tư vấn Ford Đồng Tháp",
            page_description=(
                "Tham khảo xe Ford, dự toán chi phí và liên hệ anh Huỳnh Đang Huy "
                "tại Đồng Tháp Ford để nhận tư vấn trực tiếp."
            ),
            featured_vehicles=VEHICLES[:4],
            promotions=PROMOTIONS,
            faqs=FAQS[:3],
        ),
    )


@router.get("/anh-huy", response_class=HTMLResponse)
async def about_huy(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/about.html",
        page_context(
            request,
            page_title="Anh Huỳnh Đang Huy - Tư vấn bán hàng Ford",
            page_description=(
                "Thông tin liên hệ, vai trò và cách anh Huy hỗ trợ "
                "khách hàng Ford tại Đồng Tháp."
            ),
        ),
    )


@router.get("/xe", response_class=HTMLResponse)
async def vehicles(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/vehicles.html",
        page_context(
            request,
            page_title="Danh sách xe Ford tham khảo",
            page_description=(
                "Xem các dòng xe Ford, giá tham khảo và gửi yêu cầu báo giá "
                "cho anh Huy."
            ),
        ),
    )


@router.get("/xe/{slug}", response_class=HTMLResponse)
async def vehicle_detail(request: Request, slug: str):
    vehicle = get_vehicle(slug)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return templates.TemplateResponse(
        request,
        "pages/vehicle_detail.html",
        page_context(
            request,
            vehicle=vehicle,
            page_title=f"{vehicle.name} - Giá tham khảo và tư vấn",
            page_description=(
                f"Thông tin {vehicle.name}, phiên bản, giá tham khảo "
                "và form liên hệ anh Huy."
            ),
        ),
    )


@router.get("/so-sanh", response_class=HTMLResponse)
async def compare(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/compare.html",
        page_context(
            request,
            page_title="So sánh nhanh xe Ford",
            page_description="So sánh nhanh các dòng xe Ford theo giá, nhóm xe và nhu cầu sử dụng.",
        ),
    )


@router.get("/bang-gia", response_class=HTMLResponse)
async def price_table(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/prices.html",
        page_context(
            request,
            page_title="Bảng giá Ford tham khảo",
            page_description=(
                "Bảng giá Ford tham khảo có nguồn và ngày kiểm tra, "
                "cần anh Huy xác nhận trước khi chốt."
            ),
        ),
    )


@router.get("/du-toan-lan-banh", response_class=HTMLResponse)
async def on_road_calculator(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/on_road.html",
        page_context(
            request,
            page_title="Dự toán chi phí lăn bánh Ford",
            page_description="Ước tính chi phí lăn bánh tham khảo và gửi phương án cho anh Huy.",
            assumptions=ON_ROAD_ASSUMPTIONS,
        ),
    )


@router.get("/du-toan-tra-gop", response_class=HTMLResponse)
async def loan_calculator(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/loan.html",
        page_context(
            request,
            page_title="Dự toán trả góp xe Ford",
            page_description="Ước tính trả góp xe Ford, không phải cam kết duyệt vay.",
        ),
    )


@router.get("/uu-dai", response_class=HTMLResponse)
async def promotions(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/promotions.html",
        page_context(
            request,
            page_title="Ưu đãi Ford cần xác nhận",
            page_description="Xem các nhóm ưu đãi tham khảo và gửi yêu cầu để anh Huy xác nhận.",
            promotions=PROMOTIONS,
        ),
    )


@router.get("/faq", response_class=HTMLResponse)
async def faq(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/faq.html",
        page_context(
            request,
            page_title="Câu hỏi thường gặp khi mua xe Ford",
            page_description="FAQ về giá, lăn bánh, trả góp, lái thử và liên hệ anh Huy.",
            faqs=FAQS,
        ),
    )


@router.get("/tro-ly-ai", response_class=HTMLResponse)
async def ai_assistant(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/ai_assistant.html",
        page_context(
            request,
            page_title="Trợ lý AI tư vấn Ford",
            page_description=(
                "Hỏi AI về xe Ford, giá tham khảo, lăn bánh, trả góp và chuyển yêu cầu "
                "cho anh Huy khi cần xác nhận trực tiếp."
            ),
        ),
    )


@router.get("/lien-he", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/contact.html",
        page_context(
            request,
            page_title="Liên hệ anh Huy Ford Đồng Tháp",
            page_description="Gọi, Zalo, email, Facebook hoặc gửi form để anh Huy liên hệ lại.",
        ),
    )


@router.get("/lai-thu", response_class=HTMLResponse)
async def test_drive(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/test_drive.html",
        page_context(
            request,
            page_title="Đăng ký lái thử Ford",
            page_description=(
                "Để lại thông tin xe, khu vực và thời gian mong muốn "
                "để anh Huy xác nhận lịch."
            ),
        ),
    )


@router.get("/bao-gia", response_class=HTMLResponse)
async def quote(request: Request):
    return templates.TemplateResponse(
        request,
        "pages/quote.html",
        page_context(
            request,
            page_title="Nhận báo giá Ford từ anh Huy",
            page_description=(
                "Gửi xe quan tâm và số điện thoại để anh Huy kiểm tra giá, "
                "ưu đãi và gọi lại."
            ),
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
