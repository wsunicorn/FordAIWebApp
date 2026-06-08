from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routers import admin, api, pages

try:
    import sentry_sdk
except ImportError:  # pragma: no cover - optional dependency during local setup
    sentry_sdk = None


def configure_error_tracking() -> None:
    if not settings.sentry_dsn or sentry_sdk is None:
        return

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.app_env,
        traces_sample_rate=settings.sentry_traces_sample_rate,
        send_default_pii=False,
    )


def create_app() -> FastAPI:
    configure_error_tracking()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
        version="0.1.0",
        docs_url="/docs" if settings.app_debug else None,
        redoc_url="/redoc" if settings.app_debug else None,
    )

    static_dir = Path("app/static")
    assets_dir = Path("assets")

    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.middleware("http")
    async def launch_headers_and_redirects(request, call_next):
        canonical_url = str(settings.app_url).rstrip("/")
        canonical_host = settings.app_url.host
        request_host = request.url.hostname
        if (
            settings.canonical_redirect
            and request.method in {"GET", "HEAD"}
            and canonical_host
            and request_host
            and request_host != canonical_host
        ):
            target = f"{canonical_url}{request.url.path}"
            if request.url.query:
                target = f"{target}?{request.url.query}"
            return RedirectResponse(target, status_code=308)

        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault(
            "Permissions-Policy",
            "camera=(), microphone=(), geolocation=()",
        )
        if settings.app_env.strip().lower() == "production" and canonical_url.startswith("https://"):
            response.headers.setdefault(
                "Strict-Transport-Security",
                "max-age=31536000; includeSubDomains",
            )
        return response

    app.include_router(pages.router)
    app.include_router(admin.router)
    app.include_router(api.router, prefix="/api")

    return app


app = create_app()
