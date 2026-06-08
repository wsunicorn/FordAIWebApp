from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    category: Mapped[str] = mapped_column(String(80))
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source_updated_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    review_due_at: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    approval_status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    freshness_status: Mapped[str] = mapped_column(String(40), default="review_due", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    variants: Mapped[list["VehicleVariant"]] = relationship(back_populates="vehicle")
    prices: Mapped[list["VehiclePrice"]] = relationship(back_populates="vehicle")


class VehicleVariant(Base):
    __tablename__ = "vehicle_variants"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    vehicle_id: Mapped[str] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"),
        index=True,
    )
    slug: Mapped[str] = mapped_column(String(120), index=True)
    name: Mapped[str] = mapped_column(String(160))
    engine: Mapped[str | None] = mapped_column(String(160), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    vehicle: Mapped[Vehicle] = relationship(back_populates="variants")
    prices: Mapped[list["VehiclePrice"]] = relationship(back_populates="variant")


class VehiclePrice(Base):
    __tablename__ = "vehicle_prices"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    vehicle_id: Mapped[str] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"),
        index=True,
    )
    variant_id: Mapped[str | None] = mapped_column(
        ForeignKey("vehicle_variants.id", ondelete="CASCADE"),
        nullable=True,
    )
    price_vnd: Mapped[int] = mapped_column(Integer)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source_updated_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    effective_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    review_due_at: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    freshness_status: Mapped[str] = mapped_column(String(40), default="review_due", index=True)

    vehicle: Mapped[Vehicle] = relationship(back_populates="prices")
    variant: Mapped[VehicleVariant | None] = relationship(back_populates="prices")
