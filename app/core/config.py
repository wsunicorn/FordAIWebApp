from functools import lru_cache

from pydantic import AnyUrl, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError

INSECURE_SECRET_MARKERS = ("change-me", "dev-only", "admin-dev")
PLACEHOLDER_MARKERS = ("<", ">", "paste-", "render-postgres-internal-database-url")


class Settings(BaseSettings):
    app_name: str = "Huynh Dang Huy Ford AI WebApp"
    app_env: str = "development"
    app_debug: bool = True
    app_url: AnyUrl = "http://127.0.0.1:8000"
    canonical_redirect: bool = False
    secret_key: str = Field(default="dev-only-change-me", min_length=8)

    database_url: str = "sqlite+aiosqlite:///./local.db"
    database_echo: bool = False

    sales_name: str = "Huynh Dang Huy"
    sales_title: str = "Tu Van Ban Hang"
    sales_dealership: str = "Dong Thap Ford"
    sales_phone: str = "0766994952"
    sales_zalo: str = "0818655369"
    sales_email: str = "hh753741@gmail.com"
    sales_facebook_url: str = "https://www.facebook.com/share/1X2vMYQ3T4/?mibextid=wwXIfr"

    source_site_url: str = "https://dongthapford.com/"
    revalidation_secret: str = "dev-revalidation-secret-change-me"
    ai_provider: str = "gemini"
    ai_api_key: str | None = None
    ai_model: str = "gemini-2.5-flash-lite"
    ai_daily_quota: int = 500
    ai_temperature: float = 0.2
    ai_max_output_tokens: int = 700
    ai_request_timeout_seconds: float = 20.0

    admin_username: str = "admin"
    admin_password: str = "admin-dev-change-me"
    admin_session_ttl_seconds: int = 43_200
    ga_measurement_id: str | None = None
    sentry_dsn: str | None = None
    sentry_traces_sample_rate: float = 0.1

    model_config = SettingsConfigDict(
        env_file=(".env.example", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("database_url")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        normalized_value = value.strip()
        if any(marker in normalized_value.lower() for marker in PLACEHOLDER_MARKERS):
            raise ValueError("DATABASE_URL still contains a placeholder")
        if value.startswith("postgres://"):
            normalized_value = value.replace("postgres://", "postgresql+psycopg://", 1)
        if value.startswith("postgresql://"):
            normalized_value = value.replace("postgresql://", "postgresql+psycopg://", 1)
        try:
            make_url(normalized_value)
        except ArgumentError as exc:
            raise ValueError("DATABASE_URL must be a valid SQLAlchemy database URL") from exc
        return normalized_value

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        if self.app_env.strip().lower() != "production":
            return self

        app_url = str(self.app_url).rstrip("/")
        insecure_values = {
            "SECRET_KEY": self.secret_key,
            "ADMIN_PASSWORD": self.admin_password,
            "REVALIDATION_SECRET": self.revalidation_secret,
        }
        for name, value in insecure_values.items():
            normalized = value.strip().lower()
            if len(value) < 32 or any(marker in normalized for marker in INSECURE_SECRET_MARKERS):
                raise ValueError(f"{name} must be a strong production secret")

        if self.app_debug:
            raise ValueError("APP_DEBUG must be false in production")
        if "localhost" in app_url or "127.0.0.1" in app_url:
            raise ValueError("APP_URL must be the public canonical URL in production")
        if self.database_url.startswith("sqlite"):
            raise ValueError("DATABASE_URL must use PostgreSQL in production")
        if self.sentry_traces_sample_rate < 0 or self.sentry_traces_sample_rate > 1:
            raise ValueError("SENTRY_TRACES_SAMPLE_RATE must be between 0 and 1")

        return self

    @property
    def sales(self) -> dict[str, str]:
        return {
            "name": self.sales_name,
            "title": self.sales_title,
            "dealership": self.sales_dealership,
            "phone": self.sales_phone,
            "zalo": self.sales_zalo,
            "zalo_url": f"https://zalo.me/{self.sales_zalo}",
            "email": self.sales_email,
            "facebook_url": self.sales_facebook_url,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
