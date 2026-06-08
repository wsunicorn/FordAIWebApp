from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.data.site_content import (
    FAQS,
    PRICE_SOURCE_URL,
    PROMOTIONS,
    VEHICLES,
    Variant,
    Vehicle,
    format_vnd,
)
from app.models import ContentItem
from app.models.vehicle import Vehicle as VehicleModel

PUBLIC_APPROVAL_STATUSES = ("approved", "needs_confirmation")
PUBLIC_FRESHNESS_STATUSES = ("fresh", "review_due")

PROMOTION_STATUS_LABELS = {
    "approved": "Tham khao",
    "needs_confirmation": "Can anh Huy xac nhan",
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
    return db_vehicle.summary or db_vehicle.category or "Can anh Huy tu van them"


def _to_public_vehicle(db_vehicle: VehicleModel) -> Vehicle | None:
    static_vehicle = _static_vehicle(db_vehicle.slug)
    prices_by_variant_id = {
        price.variant_id: price
        for price in db_vehicle.prices
        if price.variant_id
    }
    public_variants: list[Variant] = []

    for db_variant in sorted(db_vehicle.variants, key=lambda variant: variant.sort_order):
        db_price = prices_by_variant_id.get(db_variant.id)
        static_variant = _static_variant(static_vehicle, db_variant.name)
        if db_price:
            price_vnd = db_price.price_vnd
        elif static_variant:
            price_vnd = static_variant.price_vnd
        else:
            price_vnd = None

        if price_vnd is None:
            continue

        engine = db_variant.engine or (
            static_variant.engine if static_variant else "Can cap nhat"
        )
        public_variants.append(
            Variant(
                name=db_variant.name,
                price_vnd=price_vnd,
                engine=engine,
                drivetrain=static_variant.drivetrain if static_variant else "Anh Huy xac nhan",
            )
        )

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


async def public_promotions(session: AsyncSession) -> tuple[dict[str, str], ...]:
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
        {
            "title": item.title,
            "summary": item.body or "",
            "status": PROMOTION_STATUS_LABELS.get(item.approval_status, item.approval_status),
            "source_url": item.source_url or PRICE_SOURCE_URL,
        }
        for item in items
    )
    return promotions or PROMOTIONS


async def public_faqs(session: AsyncSession) -> tuple[dict[str, str], ...]:
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
    return faqs or FAQS
