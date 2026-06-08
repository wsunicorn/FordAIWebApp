import asyncio
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import select

from app.core.config import Settings, settings
from app.db.session import AsyncSessionLocal
from app.main import app
from app.models import AuditLog, ContentItem, Vehicle, VehiclePrice, VehicleVariant

client = TestClient(app)


def latest_audit_log(action: str) -> AuditLog | None:
    async def _get() -> AuditLog | None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(AuditLog)
                .where(AuditLog.action == action)
                .order_by(AuditLog.created_at.desc())
                .limit(1)
            )
            return result.scalars().first()

    return asyncio.run(_get())


def upsert_public_admin_content() -> None:
    async def _upsert() -> None:
        async with AsyncSessionLocal() as session:
            faq_result = await session.execute(
                select(ContentItem).where(ContentItem.title == "Pytest admin FAQ bridge")
            )
            faq = faq_result.scalars().first()
            if not faq:
                faq = ContentItem(kind="faq", title="Pytest admin FAQ bridge")
                session.add(faq)

            faq.body = "Public FAQ rendered from approved admin content."
            faq.approval_status = "approved"
            faq.freshness_status = "fresh"

            vehicle_result = await session.execute(
                select(Vehicle).where(Vehicle.slug == "pytest-public-bridge")
            )
            vehicle = vehicle_result.scalars().first()
            if not vehicle:
                vehicle = Vehicle(
                    slug="pytest-public-bridge",
                    name="Pytest Public Bridge",
                    category="SUV",
                )
                session.add(vehicle)
                await session.flush()

            vehicle.name = "Pytest Public Bridge"
            vehicle.category = "SUV"
            vehicle.summary = "Approved admin vehicle visible on public catalog."
            vehicle.approval_status = "approved"
            vehicle.freshness_status = "fresh"

            variant_result = await session.execute(
                select(VehicleVariant).where(
                    VehicleVariant.vehicle_id == vehicle.id,
                    VehicleVariant.slug == "pytest-public-bridge-base",
                )
            )
            variant = variant_result.scalars().first()
            if not variant:
                variant = VehicleVariant(
                    vehicle_id=vehicle.id,
                    slug="pytest-public-bridge-base",
                    name="Bridge Base",
                )
                session.add(variant)
                await session.flush()

            variant.name = "Bridge Base"
            variant.engine = "Test engine"
            variant.sort_order = 0

            price_result = await session.execute(
                select(VehiclePrice).where(VehiclePrice.variant_id == variant.id)
            )
            price = price_result.scalars().first()
            if not price:
                price = VehiclePrice(
                    vehicle_id=vehicle.id,
                    variant_id=variant.id,
                    price_vnd=999_000_000,
                )
                session.add(price)

            price.price_vnd = 999_000_000
            price.freshness_status = "fresh"
            await session.commit()

    asyncio.run(_upsert())


def first_vehicle_id() -> str | None:
    async def _get() -> str | None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Vehicle.id).limit(1))
            return result.scalars().first()

    return asyncio.run(_get())


def test_health_endpoint() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_database_health_endpoint() -> None:
    response = client.get("/api/health/db")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_provider_postgres_url_is_normalized_for_async_sqlalchemy() -> None:
    app_settings = Settings(database_url="postgres://user:pass@example.com:5432/app")
    assert app_settings.database_url == "postgresql+psycopg://user:pass@example.com:5432/app"


def test_production_settings_reject_insecure_defaults() -> None:
    with pytest.raises(ValidationError):
        Settings(
            app_env="production",
            app_debug=False,
            app_url="https://example.com",
            database_url="postgres://user:pass@example.com:5432/app",
            secret_key="change-me-before-production",
            admin_password="change-me-before-production",
            revalidation_secret="change-me-before-production",
        )


def test_database_url_rejects_placeholders() -> None:
    with pytest.raises(ValidationError):
        Settings(database_url="<render-postgres-internal-database-url>")


def test_database_url_rejects_blank_value() -> None:
    with pytest.raises(ValidationError):
        Settings(database_url="")


def test_home_renders() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Huỳnh Đang Huy" in response.text
    assert "Đồng Tháp Ford" in response.text


def test_home_head_probe_returns_ok() -> None:
    response = client.head("/")
    assert response.status_code == 200


def test_public_mvp_pages_render() -> None:
    routes = [
        "/anh-huy",
        "/xe",
        "/xe/ford-territory",
        "/so-sanh",
        "/bang-gia",
        "/du-toan-lan-banh",
        "/du-toan-tra-gop",
        "/uu-dai",
        "/faq",
        "/tro-ly-ai",
        "/lien-he",
        "/lai-thu",
        "/bao-gia",
    ]

    for route in routes:
        response = client.get(route)
        assert response.status_code == 200, route


def test_vehicle_detail_404() -> None:
    response = client.get("/xe/khong-co-xe-nay")
    assert response.status_code == 404


def test_seo_files_render() -> None:
    robots = client.get("/robots.txt")
    assert robots.status_code == 200
    assert "Sitemap:" in robots.text

    sitemap = client.get("/sitemap.xml")
    assert sitemap.status_code == 200
    assert "<loc>" in sitemap.text
    assert "/bang-gia" in sitemap.text


def test_seo_canonical_and_admin_noindex() -> None:
    response = client.get("/bang-gia")
    assert response.status_code == 200
    canonical = f'{str(settings.app_url).rstrip("/")}/bang-gia'
    assert f'<link rel="canonical" href="{canonical}"' in response.text
    assert f'<meta property="og:url" content="{canonical}"' in response.text
    assert "/assets/brand/favicon.svg" in response.text

    admin_login = client.get("/admin/login")
    assert admin_login.status_code == 200
    assert '<meta name="robots" content="noindex,nofollow"' in admin_login.text
    assert "/assets/brand/favicon.svg" in admin_login.text


def test_favicon_routes_render() -> None:
    fallback = client.get("/favicon.ico")
    assert fallback.status_code == 200
    assert "image/svg+xml" in fallback.headers["content-type"]
    assert "<svg" in fallback.text

    favicon = client.get("/assets/brand/favicon.svg")
    assert favicon.status_code == 200
    assert "image/svg+xml" in favicon.headers["content-type"]
    assert "<svg" in favicon.text


def test_public_html_uses_launch_safe_branding_and_media() -> None:
    routes = ["/", "/anh-huy", "/xe", "/xe/ford-territory", "/tro-ly-ai", "/lien-he"]
    banned_fragments = [
        "upload.wikimedia.org",
        "Ford_Motor_Company_Logo",
        "Ford Logo",
        "placehold.co",
        "images.unsplash.com",
        "Đại lý uỷ quyền chính thức của Ford Việt Nam",
        "Kênh tư vấn cá nhân chính thức",
    ]

    for route in routes:
        response = client.get(route)
        assert response.status_code == 200, route
        for fragment in banned_fragments:
            assert fragment not in response.text, f"{fragment} leaked in {route}"

    assert "/assets/brand/huy-dang-huy-logo.svg" in client.get("/").text


def test_static_source_quality_gates() -> None:
    template_text = "\n".join(
        path.read_text(encoding="utf-8") for path in Path("app/templates").rglob("*.html")
    )
    css_source = Path("app/static/css/input.css").read_text(encoding="utf-8")
    js_source = Path("app/static/js/app.js").read_text(encoding="utf-8")

    for fragment in ("upload.wikimedia.org", "placehold.co", "images.unsplash.com"):
        assert fragment not in template_text

    assert "transition-all" not in css_source
    assert "transition: all" not in css_source
    assert "transition: all" not in js_source
    assert "pulse-soft" not in css_source


def test_accessibility_labels_for_phase7_surfaces() -> None:
    vehicles = client.get("/xe").text
    assert 'for="vehicle-search"' in vehicles
    assert 'id="vehicle-search"' in vehicles

    on_road = client.get("/du-toan-lan-banh").text
    assert 'for="on-road-vehicle"' in on_road
    assert 'for="physical-insurance"' in on_road

    loan = client.get("/du-toan-tra-gop").text
    assert 'for="loan-vehicle"' in loan
    assert 'for="down-payment-percent"' in loan
    assert 'for="loan-term"' in loan

    ai_page = client.get("/tro-ly-ai").text
    assert 'for="ai-message"' in ai_page
    assert 'aria-label="Gửi tin nhắn cho trợ lý AI"' in ai_page
    assert 'for="ai-handoff-name"' in ai_page
    assert 'for="ai-handoff-phone"' in ai_page


def test_admin_requires_login() -> None:
    response = client.get("/admin", follow_redirects=False)
    assert response.status_code == 303
    assert "/admin/login" in response.headers["location"]


def test_admin_login_dashboard_and_seed_routes() -> None:
    admin_client = TestClient(app)
    login = admin_client.post(
        "/admin/login",
        data={
            "username": settings.admin_username,
            "password": settings.admin_password,
            "next_path": "/admin",
        },
        follow_redirects=False,
    )
    assert login.status_code == 303

    dashboard = admin_client.get("/admin")
    assert dashboard.status_code == 200
    assert "Lead" in dashboard.text

    vehicle_seed = admin_client.post("/admin/vehicles/seed", follow_redirects=False)
    assert vehicle_seed.status_code == 303

    content_seed = admin_client.post("/admin/content/seed", follow_redirects=False)
    assert content_seed.status_code == 303

    ai_seed = admin_client.post("/admin/ai/seed", follow_redirects=False)
    assert ai_seed.status_code == 303

    vehicles_admin = admin_client.get("/admin/vehicles")
    assert vehicles_admin.status_code == 200
    assert "Xe va bang gia" in vehicles_admin.text

    vehicle_id = first_vehicle_id()
    assert vehicle_id is not None
    vehicle_detail = admin_client.get(f"/admin/vehicles/{vehicle_id}")
    assert vehicle_detail.status_code == 200
    assert "Luu xe" in vehicle_detail.text

    content_admin = admin_client.get("/admin/content")
    assert content_admin.status_code == 200
    assert "Noi dung va freshness" in content_admin.text

    ai_admin = admin_client.get("/admin/ai")
    assert ai_admin.status_code == 200
    assert "Knowledge base" in ai_admin.text

    export = admin_client.get("/admin/leads/export.csv")
    assert export.status_code == 200
    assert "full_name" in export.text


def test_admin_public_content_bridge_renders_approved_db_items() -> None:
    upsert_public_admin_content()

    vehicles = client.get("/xe")
    assert vehicles.status_code == 200
    assert "Pytest Public Bridge" in vehicles.text

    vehicle_detail = client.get("/xe/pytest-public-bridge")
    assert vehicle_detail.status_code == 200
    assert "Bridge Base" in vehicle_detail.text
    assert "999" in vehicle_detail.text

    faq = client.get("/faq")
    assert faq.status_code == 200
    assert "Pytest admin FAQ bridge" in faq.text


def test_admin_can_update_lead_status() -> None:
    admin_client = TestClient(app)
    admin_client.post(
        "/admin/login",
        data={
            "username": settings.admin_username,
            "password": settings.admin_password,
            "next_path": "/admin",
        },
    )
    lead_response = admin_client.post(
        "/api/leads",
        json={
            "full_name": "Phase 5 Test Lead",
            "phone": "0900000005",
            "vehicle_interest": "Ford Ranger",
            "area": "Dong Thap",
            "need_type": "quote",
            "note": "pytest",
        },
    )
    assert lead_response.status_code == 200
    lead_id = lead_response.json()["id"]

    update = admin_client.post(
        f"/admin/leads/{lead_id}",
        data={
            "lead_status": "contacted",
            "admin_note": "Da goi lan 1",
            "follow_up_at": "2026-06-08T09:00",
            "last_contacted_at": "2026-06-07T17:30",
        },
        follow_redirects=False,
    )
    assert update.status_code == 303

    detail = admin_client.get(f"/admin/leads/{lead_id}")
    assert detail.status_code == 200
    assert "contacted" in detail.text


def test_public_lead_form_validation_and_redirect() -> None:
    valid = client.post(
        "/lead",
        data={
            "full_name": "Phase 7 Form Lead",
            "phone": "0900000007",
            "vehicle_interest": "Ford Territory",
            "area": "Dong Thap",
            "need_type": "quote",
            "note": "pytest phase 7",
            "redirect_to": "/bao-gia",
        },
        follow_redirects=False,
    )
    assert valid.status_code == 303
    assert valid.headers["location"] == "/bao-gia?lead=success"

    missing_name = client.post(
        "/lead",
        data={"phone": "0900000007", "need_type": "quote", "redirect_to": "/bao-gia"},
    )
    assert missing_name.status_code == 422

    short_phone = client.post(
        "/lead",
        data={
            "full_name": "A",
            "phone": "123",
            "need_type": "quote",
            "redirect_to": "/bao-gia",
        },
    )
    assert short_phone.status_code == 422


def test_api_lead_validation() -> None:
    response = client.post(
        "/api/leads",
        json={
            "full_name": "A",
            "phone": "123",
            "vehicle_interest": "Ford Ranger",
            "need_type": "quote",
        },
    )
    assert response.status_code == 422


def test_revalidation_auth_and_audit_log() -> None:
    denied = client.post(
        "/api/revalidate",
        json={"secret": "wrong", "paths": ["/bang-gia"], "reason": "pytest"},
    )
    assert denied.status_code == 401

    allowed = client.post(
        "/api/revalidate",
        json={
            "secret": settings.revalidation_secret,
            "paths": ["/bang-gia"],
            "tags": ["prices"],
            "reason": "phase7-pytest",
        },
    )
    assert allowed.status_code == 200
    assert allowed.json()["paths"] == ["/bang-gia"]

    audit_log = latest_audit_log("cache.revalidate")
    assert audit_log is not None
    assert audit_log.metadata_json["reason"] == "phase7-pytest"
    assert audit_log.metadata_json["paths"] == ["/bang-gia"]


def test_admin_rejects_invalid_status_choice() -> None:
    admin_client = TestClient(app)
    admin_client.post(
        "/admin/login",
        data={
            "username": settings.admin_username,
            "password": settings.admin_password,
            "next_path": "/admin",
        },
    )
    lead_response = admin_client.post(
        "/api/leads",
        json={
            "full_name": "Phase 7 Invalid Status",
            "phone": "0900000077",
            "vehicle_interest": "Ford Everest",
            "need_type": "quote",
        },
    )
    assert lead_response.status_code == 200

    rejected = admin_client.post(
        f"/admin/leads/{lead_response.json()['id']}",
        data={"lead_status": "invalid", "admin_note": "pytest"},
    )
    assert rejected.status_code == 400

    rejected_list_filter = admin_client.get("/admin/leads?status_filter=invalid")
    assert rejected_list_filter.status_code == 400

    rejected_export_filter = admin_client.get("/admin/leads/export.csv?status_filter=invalid")
    assert rejected_export_filter.status_code == 400

    rejected_content_filter = admin_client.get("/admin/content?kind=invalid")
    assert rejected_content_filter.status_code == 400


def test_ai_chat_calculator_and_guardrail() -> None:
    calculator = client.post(
        "/api/ai/chat",
        json={"message": "Ford Everest lan banh khoang bao nhieu?"},
    )
    assert calculator.status_code == 200
    calculator_data = calculator.json()
    assert calculator_data["tool_name"] == "on_road_calculator"
    assert calculator_data["conversation_id"]

    guardrail = client.post(
        "/api/ai/chat",
        json={
            "session_id": calculator_data["session_id"],
            "message": "Giá chốt Everest còn xe giao ngay không?",
        },
    )
    assert guardrail.status_code == 200
    guardrail_data = guardrail.json()
    assert guardrail_data["handoff_required"] is True
    assert "final_price" in guardrail_data["risk_flags"]
    assert "stock" in guardrail_data["risk_flags"]


def test_ai_handoff_creates_lead() -> None:
    chat = client.post(
        "/api/ai/chat",
        json={"message": "Ford Territory lan banh khoang bao nhieu?"},
    )
    assert chat.status_code == 200
    conversation_id = chat.json()["conversation_id"]

    handoff = client.post(
        "/api/ai/handoff",
        json={
            "conversation_id": conversation_id,
            "full_name": "Phase 6 AI Test",
            "phone": "0900000066",
            "vehicle_interest": "Ford Territory",
            "area": "Dong Thap",
            "note": "pytest ai handoff",
        },
    )
    assert handoff.status_code == 200
    assert handoff.json()["ok"] is True
