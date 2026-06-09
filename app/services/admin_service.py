from __future__ import annotations

import re
import unicodedata
from datetime import date, datetime, timedelta

from sqlalchemy import delete, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.data.site_content import (
    FAQS,
    PRICE_SOURCE_URL,
    PROMOTIONS,
    SOURCE_CHECKED_AT,
    VEHICLES,
)
from app.models import AuditLog, ContentItem, Lead, Vehicle, VehiclePrice, VehicleVariant
from app.services.audit_service import write_audit_log

LEAD_STATUSES = ("new", "contacted", "quoted", "test_drive", "won", "lost")
CONTENT_KINDS = ("promotion", "faq", "article")
APPROVAL_STATUSES = ("draft", "needs_confirmation", "approved", "archived")
FRESHNESS_STATUSES = ("fresh", "review_due", "expired")
RETIRED_VEHICLE_SLUGS = ("ford-transit-limousine",)


def content_public_paths(kind: str) -> list[str]:
    if kind == "faq":
        return ["/faq"]
    if kind == "promotion":
        return ["/uu-dai"]
    return ["/uu-dai", "/faq"]


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug or "item"


def parse_optional_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def parse_optional_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)


async def lead_status_counts(session: AsyncSession) -> dict[str, int]:
    result = await session.execute(select(Lead.status, func.count(Lead.id)).group_by(Lead.status))
    counts = {status: 0 for status in LEAD_STATUSES}
    counts.update({status: count for status, count in result.all()})
    return counts


async def content_freshness_counts(session: AsyncSession) -> dict[str, int]:
    vehicle_result = await session.execute(
        select(Vehicle.freshness_status, func.count(Vehicle.id)).group_by(Vehicle.freshness_status)
    )
    price_result = await session.execute(
        select(VehiclePrice.freshness_status, func.count(VehiclePrice.id)).group_by(
            VehiclePrice.freshness_status
        )
    )
    content_result = await session.execute(
        select(ContentItem.freshness_status, func.count(ContentItem.id)).group_by(
            ContentItem.freshness_status
        )
    )

    counts = {status: 0 for status in FRESHNESS_STATUSES}
    for rows in (vehicle_result.all(), price_result.all(), content_result.all()):
        for status, count in rows:
            counts[status] = counts.get(status, 0) + count
    return counts


async def list_leads(
    session: AsyncSession,
    *,
    status: str | None = None,
    query: str | None = None,
    limit: int = 100,
) -> list[Lead]:
    statement = select(Lead).order_by(desc(Lead.created_at)).limit(limit)
    if status:
        statement = statement.where(Lead.status == status)
    if query:
        search = f"%{query.strip()}%"
        statement = statement.where(
            or_(
                Lead.full_name.ilike(search),
                Lead.phone.ilike(search),
                Lead.vehicle_interest.ilike(search),
                Lead.area.ilike(search),
            )
        )
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_lead_or_none(session: AsyncSession, lead_id: str) -> Lead | None:
    return await session.get(Lead, lead_id)


async def update_lead_care(
    session: AsyncSession,
    lead: Lead,
    *,
    status: str,
    admin_note: str | None,
    follow_up_at: datetime | None,
    last_contacted_at: datetime | None,
) -> Lead:
    lead.status = status
    lead.admin_note = admin_note or None
    lead.follow_up_at = follow_up_at
    lead.last_contacted_at = last_contacted_at
    await session.commit()
    await session.refresh(lead)
    await write_audit_log(
        session,
        action="lead.updated",
        entity_table="leads",
        entity_id=lead.id,
        metadata={
            "status": lead.status,
            "follow_up_at": lead.follow_up_at.isoformat() if lead.follow_up_at else None,
        },
    )
    return lead


async def recent_audit_logs(session: AsyncSession, *, limit: int = 30) -> list[AuditLog]:
    result = await session.execute(
        select(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit)
    )
    return list(result.scalars().all())


async def list_vehicles(session: AsyncSession) -> list[Vehicle]:
    result = await session.execute(
        select(Vehicle)
        .options(selectinload(Vehicle.variants), selectinload(Vehicle.prices))
        .order_by(Vehicle.name)
    )
    return list(result.scalars().unique().all())


async def get_vehicle_or_none(session: AsyncSession, vehicle_id: str) -> Vehicle | None:
    result = await session.execute(
        select(Vehicle)
        .where(Vehicle.id == vehicle_id)
        .options(selectinload(Vehicle.variants), selectinload(Vehicle.prices))
    )
    return result.scalars().unique().first()


async def seed_vehicles_from_source(session: AsyncSession) -> int:
    source_date = date.fromisoformat(SOURCE_CHECKED_AT)
    review_due_at = source_date + timedelta(days=14)
    effective_to = source_date + timedelta(days=45)
    source_slugs = {vehicle.slug for vehicle in VEHICLES}
    touched = 0

    await session.execute(
        delete(VehiclePrice).where(
            VehiclePrice.vehicle_id.in_(
                select(Vehicle.id).where(Vehicle.slug.in_(RETIRED_VEHICLE_SLUGS))
            )
        )
    )
    await session.execute(
        delete(VehicleVariant).where(
            VehicleVariant.vehicle_id.in_(
                select(Vehicle.id).where(Vehicle.slug.in_(RETIRED_VEHICLE_SLUGS))
            )
        )
    )
    await session.execute(delete(Vehicle).where(Vehicle.slug.in_(RETIRED_VEHICLE_SLUGS)))

    for source_vehicle in VEHICLES:
        result = await session.execute(select(Vehicle).where(Vehicle.slug == source_vehicle.slug))
        vehicle = result.scalars().first()
        if not vehicle:
            vehicle = Vehicle(
                slug=source_vehicle.slug,
                name=source_vehicle.name,
                category=source_vehicle.category,
            )
            session.add(vehicle)
            await session.flush()

        vehicle.name = source_vehicle.name
        vehicle.category = source_vehicle.category
        vehicle.summary = source_vehicle.summary
        vehicle.source_url = source_vehicle.source_url
        vehicle.source_updated_at = source_date
        vehicle.review_due_at = review_due_at
        vehicle.approval_status = "approved"
        vehicle.freshness_status = "fresh"
        touched += 1

        source_variant_slugs = {
            slugify(source_variant.name) for source_variant in source_vehicle.variants
        }
        stale_variants = await session.execute(
            select(VehicleVariant.id).where(
                VehicleVariant.vehicle_id == vehicle.id,
                VehicleVariant.slug.not_in(source_variant_slugs),
            )
        )
        stale_variant_ids = list(stale_variants.scalars().all())
        if stale_variant_ids:
            await session.execute(
                delete(VehiclePrice).where(VehiclePrice.variant_id.in_(stale_variant_ids))
            )
            await session.execute(
                delete(VehicleVariant).where(VehicleVariant.id.in_(stale_variant_ids))
            )

        for index, source_variant in enumerate(source_vehicle.variants):
            variant_slug = slugify(source_variant.name)
            variant_result = await session.execute(
                select(VehicleVariant).where(
                    VehicleVariant.vehicle_id == vehicle.id,
                    VehicleVariant.slug == variant_slug,
                )
            )
            variant = variant_result.scalars().first()
            if not variant:
                variant = VehicleVariant(
                    vehicle_id=vehicle.id,
                    slug=variant_slug,
                    name=source_variant.name,
                )
                session.add(variant)
                await session.flush()

            variant.name = source_variant.name
            variant.engine = source_variant.engine
            variant.sort_order = index

            price_result = await session.execute(
                select(VehiclePrice).where(VehiclePrice.variant_id == variant.id)
            )
            price = price_result.scalars().first()
            if not price:
                price = VehiclePrice(
                    vehicle_id=vehicle.id,
                    variant_id=variant.id,
                    price_vnd=source_variant.price_vnd,
                )
                session.add(price)

            price.price_vnd = source_variant.price_vnd
            price.source_url = source_vehicle.source_url
            price.source_updated_at = source_date
            price.effective_to = effective_to
            price.review_due_at = review_due_at
            price.freshness_status = "fresh"

    await session.commit()
    await write_audit_log(
        session,
        action="vehicles.seeded",
        entity_table="vehicles",
        metadata={
            "source": PRICE_SOURCE_URL,
            "vehicle_count": touched,
            "source_slugs": sorted(source_slugs),
        },
    )
    await write_audit_log(
        session,
        action="cache.revalidate",
        entity_table="cache",
        metadata={"paths": ["/xe", "/bang-gia", "/so-sanh"], "reason": "admin_vehicle_seed"},
    )
    return touched


async def update_vehicle(
    session: AsyncSession,
    vehicle: Vehicle,
    *,
    name: str,
    category: str,
    summary: str | None,
    source_url: str | None,
    source_updated_at: date | None,
    review_due_at: date | None,
    approval_status: str,
    freshness_status: str,
) -> Vehicle:
    vehicle.name = name
    vehicle.category = category
    vehicle.summary = summary or None
    vehicle.source_url = source_url or None
    vehicle.source_updated_at = source_updated_at
    vehicle.review_due_at = review_due_at
    vehicle.approval_status = approval_status
    vehicle.freshness_status = freshness_status
    await session.commit()
    await session.refresh(vehicle)
    await write_audit_log(
        session,
        action="vehicle.updated",
        entity_table="vehicles",
        entity_id=vehicle.id,
        metadata={"slug": vehicle.slug, "freshness_status": vehicle.freshness_status},
    )
    await write_audit_log(
        session,
        action="cache.revalidate",
        entity_table="cache",
        metadata={
            "paths": ["/xe", f"/xe/{vehicle.slug}", "/bang-gia"],
            "reason": "admin_vehicle_update",
        },
    )
    return vehicle


async def update_variant(
    session: AsyncSession,
    variant: VehicleVariant,
    *,
    name: str,
    engine: str | None,
    sort_order: int,
) -> VehicleVariant:
    variant.name = name
    variant.engine = engine or None
    variant.sort_order = sort_order
    await session.commit()
    await session.refresh(variant)
    await write_audit_log(
        session,
        action="vehicle_variant.updated",
        entity_table="vehicle_variants",
        entity_id=variant.id,
        metadata={"vehicle_id": variant.vehicle_id},
    )
    await write_audit_log(
        session,
        action="cache.revalidate",
        entity_table="cache",
        metadata={"paths": ["/xe", "/bang-gia", "/so-sanh"], "reason": "admin_variant_update"},
    )
    return variant


async def create_variant_with_price(
    session: AsyncSession,
    vehicle: Vehicle,
    *,
    name: str,
    engine: str | None,
    sort_order: int,
    price_vnd: int,
    source_url: str | None,
    source_updated_at: date | None,
    effective_to: date | None,
    review_due_at: date | None,
    freshness_status: str,
) -> VehicleVariant:
    variant = VehicleVariant(
        vehicle_id=vehicle.id,
        slug=slugify(name),
        name=name,
        engine=engine or None,
        sort_order=sort_order,
    )
    session.add(variant)
    await session.flush()
    price = VehiclePrice(
        vehicle_id=vehicle.id,
        variant_id=variant.id,
        price_vnd=price_vnd,
        source_url=source_url or vehicle.source_url,
        source_updated_at=source_updated_at,
        effective_to=effective_to,
        review_due_at=review_due_at,
        freshness_status=freshness_status,
    )
    session.add(price)
    await session.commit()
    await session.refresh(variant)
    await write_audit_log(
        session,
        action="vehicle_variant.created",
        entity_table="vehicle_variants",
        entity_id=variant.id,
        metadata={"vehicle_id": vehicle.id, "price_vnd": price_vnd},
    )
    await write_audit_log(
        session,
        action="cache.revalidate",
        entity_table="cache",
        metadata={
            "paths": ["/xe", f"/xe/{vehicle.slug}", "/bang-gia", "/so-sanh"],
            "reason": "admin_variant_create",
        },
    )
    return variant


async def delete_variant(
    session: AsyncSession,
    vehicle: Vehicle,
    variant: VehicleVariant,
) -> None:
    await session.execute(delete(VehiclePrice).where(VehiclePrice.variant_id == variant.id))
    await session.delete(variant)
    await session.commit()
    await write_audit_log(
        session,
        action="vehicle_variant.deleted",
        entity_table="vehicle_variants",
        entity_id=variant.id,
        metadata={"vehicle_id": vehicle.id, "variant_name": variant.name},
    )
    await write_audit_log(
        session,
        action="cache.revalidate",
        entity_table="cache",
        metadata={
            "paths": ["/xe", f"/xe/{vehicle.slug}", "/bang-gia", "/so-sanh"],
            "reason": "admin_variant_delete",
        },
    )


async def update_price(
    session: AsyncSession,
    price: VehiclePrice,
    *,
    price_vnd: int,
    source_url: str | None,
    source_updated_at: date | None,
    effective_to: date | None,
    review_due_at: date | None,
    freshness_status: str,
) -> VehiclePrice:
    price.price_vnd = price_vnd
    price.source_url = source_url or None
    price.source_updated_at = source_updated_at
    price.effective_to = effective_to
    price.review_due_at = review_due_at
    price.freshness_status = freshness_status
    await session.commit()
    await session.refresh(price)
    await write_audit_log(
        session,
        action="vehicle_price.updated",
        entity_table="vehicle_prices",
        entity_id=price.id,
        metadata={"vehicle_id": price.vehicle_id, "freshness_status": price.freshness_status},
    )
    await write_audit_log(
        session,
        action="cache.revalidate",
        entity_table="cache",
        metadata={"paths": ["/bang-gia", "/xe"], "reason": "admin_price_update"},
    )
    return price


async def list_content_items(
    session: AsyncSession,
    *,
    kind: str | None = None,
) -> list[ContentItem]:
    statement = select(ContentItem).order_by(ContentItem.kind, ContentItem.title)
    if kind:
        statement = statement.where(ContentItem.kind == kind)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def seed_content_from_source(session: AsyncSession) -> int:
    source_date = date.fromisoformat(SOURCE_CHECKED_AT)
    review_due_at = source_date + timedelta(days=14)
    touched = 0

    for item in PROMOTIONS:
        touched += await _upsert_content_item(
            session,
            kind="promotion",
            title=item["title"],
            body=item["summary"],
            source_url=item.get("source_url") or PRICE_SOURCE_URL,
            source_updated_at=source_date,
            review_due_at=review_due_at,
            approval_status="needs_confirmation",
            freshness_status="review_due",
        )

    for item in FAQS:
        touched += await _upsert_content_item(
            session,
            kind="faq",
            title=item["question"],
            body=item["answer"],
            source_url=PRICE_SOURCE_URL,
            source_updated_at=source_date,
            review_due_at=review_due_at,
            approval_status="approved",
            freshness_status="fresh",
        )

    await session.commit()
    await write_audit_log(
        session,
        action="content.seeded",
        entity_table="content_items",
        metadata={"count": touched, "source": PRICE_SOURCE_URL},
    )
    await write_audit_log(
        session,
        action="cache.revalidate",
        entity_table="cache",
        metadata={"paths": ["/uu-dai", "/faq"], "reason": "admin_content_seed"},
    )
    return touched


async def _upsert_content_item(
    session: AsyncSession,
    *,
    kind: str,
    title: str,
    body: str | None,
    source_url: str | None,
    source_updated_at: date | None,
    review_due_at: date | None,
    approval_status: str,
    freshness_status: str,
) -> int:
    result = await session.execute(
        select(ContentItem).where(ContentItem.kind == kind, ContentItem.title == title)
    )
    content_item = result.scalars().first()
    if not content_item:
        content_item = ContentItem(kind=kind, title=title)
        session.add(content_item)
    content_item.body = body
    content_item.source_url = source_url
    content_item.source_updated_at = source_updated_at
    content_item.review_due_at = review_due_at
    content_item.approval_status = approval_status
    content_item.freshness_status = freshness_status
    return 1


async def create_content_item(
    session: AsyncSession,
    *,
    kind: str,
    title: str,
    body: str | None,
    source_url: str | None,
    source_updated_at: date | None,
    effective_to: date | None,
    review_due_at: date | None,
    approval_status: str,
    freshness_status: str,
) -> ContentItem:
    content_item = ContentItem(
        kind=kind,
        title=title,
        body=body or None,
        source_url=source_url or None,
        source_updated_at=source_updated_at,
        effective_to=effective_to,
        review_due_at=review_due_at,
        approval_status=approval_status,
        freshness_status=freshness_status,
    )
    session.add(content_item)
    await session.commit()
    await session.refresh(content_item)
    await write_audit_log(
        session,
        action="content.created",
        entity_table="content_items",
        entity_id=content_item.id,
        metadata={"kind": content_item.kind},
    )
    await write_audit_log(
        session,
        action="cache.revalidate",
        entity_table="cache",
        metadata={
            "paths": content_public_paths(content_item.kind),
            "reason": "admin_content_create",
        },
    )
    return content_item


async def update_content_item(
    session: AsyncSession,
    content_item: ContentItem,
    *,
    kind: str,
    title: str,
    body: str | None,
    source_url: str | None,
    source_updated_at: date | None,
    effective_to: date | None,
    review_due_at: date | None,
    approval_status: str,
    freshness_status: str,
) -> ContentItem:
    content_item.kind = kind
    content_item.title = title
    content_item.body = body or None
    content_item.source_url = source_url or None
    content_item.source_updated_at = source_updated_at
    content_item.effective_to = effective_to
    content_item.review_due_at = review_due_at
    content_item.approval_status = approval_status
    content_item.freshness_status = freshness_status
    await session.commit()
    await session.refresh(content_item)
    await write_audit_log(
        session,
        action="content.updated",
        entity_table="content_items",
        entity_id=content_item.id,
        metadata={"kind": content_item.kind, "freshness_status": content_item.freshness_status},
    )
    await write_audit_log(
        session,
        action="cache.revalidate",
        entity_table="cache",
        metadata={
            "paths": content_public_paths(content_item.kind),
            "reason": "admin_content_update",
        },
    )
    return content_item
