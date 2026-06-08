from pathlib import Path

from fastapi.templating import Jinja2Templates

from app.core.config import settings

templates = Jinja2Templates(directory=Path("app/templates"))


def common_context() -> dict[str, object]:
    return {
        "settings": settings,
        "base_url": str(settings.app_url).rstrip("/"),
        "sales": settings.sales,
        "source_site_url": settings.source_site_url,
        "ga_measurement_id": settings.ga_measurement_id,
    }
