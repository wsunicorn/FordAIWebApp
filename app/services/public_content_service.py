from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.data.site_content import (
    FAQS,
    PRICE_SOURCE_URL,
    PROMOTIONS,
    SOURCE_CHECKED_AT,
    VEHICLES,
    Variant,
    Vehicle,
    format_vnd,
)
from app.models import ContentItem
from app.models.vehicle import Vehicle as VehicleModel
from app.services.i18n_service import DEFAULT_LOCALE, normalize_locale

PUBLIC_APPROVAL_STATUSES = ("approved", "needs_confirmation")
PUBLIC_FRESHNESS_STATUSES = ("fresh", "review_due")
SOURCE_CHECKED_DATE = date.fromisoformat(SOURCE_CHECKED_AT)
RETIRED_VEHICLE_SLUGS = ("ford-transit-limousine",)
RETIRED_VARIANT_NAMES = {
    "ford-everest": {
        "everest ambiente",
        "everest ambient",
        "everest sport se",
        "everest titanium",
        "everest platinum",
    },
    "ford-ranger": {
        "ranger xl 4x4 mt",
        "ranger sport",
        "ranger stormtrak",
        "ranger stomtrak",
        "ranger wildtrak 4x4",
        "ranger raptor",
    },
}

PROMOTION_STATUS_LABELS = {
    "vi": {
        "approved": "Tham khảo",
        "needs_confirmation": "Cần anh Huy xác nhận",
    },
    "en": {
        "approved": "Reference",
        "needs_confirmation": "Needs Huy's confirmation",
    },
}
STATIC_PROMOTION_STATUS_TRANSLATIONS = {
    "en": {
        "Cần anh Huy xác nhận": "Needs Huy's confirmation",
        "Tham khảo": "Reference",
        "Cần xác nhận lịch": "Schedule confirmation needed",
    }
}
PROMOTION_TRANSLATIONS = {
    "en": {
        "Khuyến mãi áp dụng theo từng phiên bản": {
            "title": "Offers apply by variant",
            "summary": "The source records offers that change by model, variant and timing.",
        },
        "Hỗ trợ trả góp và tư vấn hồ sơ": {
            "title": "Financing support and application advice",
            "summary": (
                "Loan results depend on the bank, application profile and program "
                "at the time of processing."
            ),
        },
        "Đăng ký lái thử": {
            "title": "Test-drive registration",
            "summary": "Leave your information so Huy can check schedule and supported area.",
        },
    }
}
FAQ_TRANSLATIONS = {
    "en": {
        "Giá xe trên website có phải giá chốt không?": {
            "question": "Are prices on this website final prices?",
            "answer": (
                "No. These are reference prices from recorded sources. Final price, "
                "offers, color availability and delivery time need direct confirmation "
                "from Huy."
            ),
        },
        "Có thể tính lăn bánh tại Đồng Tháp không?": {
            "question": "Can I estimate on-road cost in Dong Thap?",
            "answer": (
                "Yes. The estimate can use the current Other area group. Actual fees "
                "at registration time need confirmation."
            ),
        },
        "Trả góp có được duyệt chắc chắn không?": {
            "question": "Is financing approval guaranteed?",
            "answer": (
                "No commitment can be made on the website. The calculator only "
                "estimates payments using assumed interest rates, and the bank reviews "
                "the loan application."
            ),
        },
        "Anh Huy có hỗ trợ ngoài Đồng Tháp không?": {
            "question": "Does Huy support customers outside Dong Thap?",
            "answer": (
                "Nearby areas may be supported depending on the case. Leave your "
                "information so Huy can check the suitable support option."
            ),
        },
    }
}


def _static_vehicle(slug: str) -> Vehicle | None:
    return next((vehicle for vehicle in VEHICLES if vehicle.slug == slug), None)


def _static_variant(static_vehicle: Vehicle | None, name: str) -> Variant | None:
    if not static_vehicle:
        return None
    normalized_name = name.strip().lower()
    return next(
        (
            variant
            for variant in static_vehicle.variants
            if variant.name.strip().lower() == normalized_name
        ),
        None,
    )


def _vehicle_tags(db_vehicle: VehicleModel, static_vehicle: Vehicle | None) -> tuple[str, ...]:
    if static_vehicle:
        return static_vehicle.tags

    raw_tags = [db_vehicle.category, db_vehicle.name]
    tags = tuple(tag for tag in raw_tags if tag)
    return tags[:3] or ("Ford",)


def _vehicle_fit(db_vehicle: VehicleModel, static_vehicle: Vehicle | None) -> str:
    if static_vehicle:
        return static_vehicle.fit
    return db_vehicle.summary or db_vehicle.category or "Cần anh Huy tư vấn thêm"


def _db_price_is_current(db_price_source_updated_at: date | None) -> bool:
    return (
        db_price_source_updated_at is not None
        and db_price_source_updated_at >= SOURCE_CHECKED_DATE
    )


def _promotion_status_label(status: str, locale: str) -> str:
    normalized_locale = normalize_locale(locale)
    return PROMOTION_STATUS_LABELS[normalized_locale].get(status, status)


def _localize_promotion(
    promotion: dict[str, str],
    locale: str,
) -> dict[str, str]:
    normalized_locale = normalize_locale(locale)
    if normalized_locale == DEFAULT_LOCALE:
        return promotion

    translated = PROMOTION_TRANSLATIONS.get(normalized_locale, {}).get(
        promotion["title"],
        {},
    )
    status = STATIC_PROMOTION_STATUS_TRANSLATIONS.get(normalized_locale, {}).get(
        promotion["status"],
        promotion["status"],
    )
    return {
        **promotion,
        "title": translated.get("title", promotion["title"]),
        "summary": translated.get("summary", promotion["summary"]),
        "status": status,
    }


def _localize_faq(faq: dict[str, str], locale: str) -> dict[str, str]:
    normalized_locale = normalize_locale(locale)
    if normalized_locale == DEFAULT_LOCALE:
        return faq

    translated = FAQ_TRANSLATIONS.get(normalized_locale, {}).get(faq["question"], {})
    return {
        **faq,
        "question": translated.get("question", faq["question"]),
        "answer": translated.get("answer", faq["answer"]),
    }


def _to_public_vehicle(db_vehicle: VehicleModel) -> Vehicle | None:
    static_vehicle = _static_vehicle(db_vehicle.slug)
    prices_by_variant_id = {
        price.variant_id: price
        for price in db_vehicle.prices
        if price.variant_id
    }
    public_variants: list[Variant] = []
    public_variant_names: set[str] = set()

    for db_variant in sorted(db_vehicle.variants, key=lambda variant: variant.sort_order):
        normalized_variant_name = db_variant.name.strip().lower()
        if normalized_variant_name in RETIRED_VARIANT_NAMES.get(db_vehicle.slug, set()):
            continue

        db_price = prices_by_variant_id.get(db_variant.id)
        static_variant = _static_variant(static_vehicle, db_variant.name)
        if db_price and (not static_variant or _db_price_is_current(db_price.source_updated_at)):
            price_vnd = db_price.price_vnd
        elif static_variant:
            price_vnd = static_variant.price_vnd
        else:
            price_vnd = None

        if price_vnd is None:
            continue

        engine = db_variant.engine or (
            static_variant.engine if static_variant else "Cần cập nhật"
        )
        public_variants.append(
            Variant(
                name=db_variant.name,
                price_vnd=price_vnd,
                engine=engine,
                drivetrain=static_variant.drivetrain if static_variant else "Anh Huy xác nhận",
            )
        )
        public_variant_names.add(normalized_variant_name)

    if static_vehicle:
        for static_variant in static_vehicle.variants:
            normalized_static_name = static_variant.name.strip().lower()
            if normalized_static_name in public_variant_names:
                continue
            public_variants.append(static_variant)
            public_variant_names.add(normalized_static_name)

    if not public_variants and static_vehicle:
        public_variants = list(static_vehicle.variants)

    if not public_variants:
        return None

    return Vehicle(
        slug=db_vehicle.slug,
        name=db_vehicle.name,
        category=db_vehicle.category,
        summary=db_vehicle.summary or (static_vehicle.summary if static_vehicle else ""),
        fit=_vehicle_fit(db_vehicle, static_vehicle),
        source_url=db_vehicle.source_url
        or (static_vehicle.source_url if static_vehicle else PRICE_SOURCE_URL),
        variants=tuple(public_variants),
        tags=_vehicle_tags(db_vehicle, static_vehicle),
        image_path=static_vehicle.image_path if static_vehicle else None,
        image_source_url=static_vehicle.image_source_url if static_vehicle else None,
    )


async def public_vehicles(session: AsyncSession) -> tuple[Vehicle, ...]:
    result = await session.execute(
        select(VehicleModel)
        .where(
            VehicleModel.slug.not_in(RETIRED_VEHICLE_SLUGS),
            VehicleModel.approval_status.in_(PUBLIC_APPROVAL_STATUSES),
            VehicleModel.freshness_status.in_(PUBLIC_FRESHNESS_STATUSES),
        )
        .options(selectinload(VehicleModel.variants), selectinload(VehicleModel.prices))
        .order_by(VehicleModel.name)
    )
    db_vehicles = result.scalars().unique().all()
    vehicles = tuple(
        public_vehicle
        for db_vehicle in db_vehicles
        if (public_vehicle := _to_public_vehicle(db_vehicle)) is not None
    )
    return vehicles or VEHICLES


async def public_vehicle(session: AsyncSession, slug: str) -> Vehicle | None:
    vehicles = await public_vehicles(session)
    return next((vehicle for vehicle in vehicles if vehicle.slug == slug), None)


def public_vehicle_options(vehicles: tuple[Vehicle, ...]) -> list[dict[str, str | int]]:
    return [
        {
            "slug": vehicle.slug,
            "name": vehicle.name,
            "price": vehicle.price_from,
            "price_label": format_vnd(vehicle.price_from),
        }
        for vehicle in vehicles
    ]


async def public_promotions(
    session: AsyncSession,
    locale: str = DEFAULT_LOCALE,
) -> tuple[dict[str, str], ...]:
    result = await session.execute(
        select(ContentItem)
        .where(
            ContentItem.kind == "promotion",
            ContentItem.approval_status.in_(PUBLIC_APPROVAL_STATUSES),
            ContentItem.freshness_status.in_(PUBLIC_FRESHNESS_STATUSES),
        )
        .order_by(ContentItem.updated_at.desc(), ContentItem.title)
    )
    items = result.scalars().all()
    promotions = tuple(
        _localize_promotion(
            {
                "title": item.title,
                "summary": item.body or "",
                "status": _promotion_status_label(item.approval_status, locale),
                "source_url": item.source_url or PRICE_SOURCE_URL,
            },
            locale,
        )
        for item in items
    )
    return promotions or tuple(
        _localize_promotion(promotion, locale) for promotion in PROMOTIONS
    )


async def public_faqs(
    session: AsyncSession,
    locale: str = DEFAULT_LOCALE,
) -> tuple[dict[str, str], ...]:
    result = await session.execute(
        select(ContentItem)
        .where(
            ContentItem.kind == "faq",
            ContentItem.approval_status == "approved",
            ContentItem.freshness_status.in_(PUBLIC_FRESHNESS_STATUSES),
        )
        .order_by(ContentItem.updated_at.desc(), ContentItem.title)
    )
    items = result.scalars().all()
    faqs = tuple({"question": item.title, "answer": item.body or ""} for item in items)
    localized_faqs = tuple(_localize_faq(faq, locale) for faq in faqs)
    return localized_faqs or tuple(_localize_faq(faq, locale) for faq in FAQS)
