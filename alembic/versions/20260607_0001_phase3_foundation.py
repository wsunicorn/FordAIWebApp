"""phase3 foundation

Revision ID: 20260607_0001
Revises:
Create Date: 2026-06-07
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260607_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "vehicles",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("slug", sa.String(length=120), nullable=False, unique=True),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("source_updated_at", sa.Date(), nullable=True),
        sa.Column("approval_status", sa.String(length=40), nullable=False),
        sa.Column("freshness_status", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_vehicles_slug", "vehicles", ["slug"])
    op.create_index("ix_vehicles_approval_status", "vehicles", ["approval_status"])
    op.create_index("ix_vehicles_freshness_status", "vehicles", ["freshness_status"])

    op.create_table(
        "vehicle_variants",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("vehicle_id", sa.String(length=36), sa.ForeignKey("vehicles.id"), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("engine", sa.String(length=160), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
    )
    op.create_index("ix_vehicle_variants_vehicle_id", "vehicle_variants", ["vehicle_id"])
    op.create_index("ix_vehicle_variants_slug", "vehicle_variants", ["slug"])

    op.create_table(
        "vehicle_prices",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("vehicle_id", sa.String(length=36), sa.ForeignKey("vehicles.id"), nullable=False),
        sa.Column(
            "variant_id",
            sa.String(length=36),
            sa.ForeignKey("vehicle_variants.id"),
            nullable=True,
        ),
        sa.Column("price_vnd", sa.Integer(), nullable=False),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("source_updated_at", sa.Date(), nullable=True),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column("freshness_status", sa.String(length=40), nullable=False),
    )
    op.create_index("ix_vehicle_prices_vehicle_id", "vehicle_prices", ["vehicle_id"])

    op.create_table(
        "leads",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("full_name", sa.String(length=160), nullable=False),
        sa.Column("phone", sa.String(length=40), nullable=False),
        sa.Column("vehicle_interest", sa.String(length=160), nullable=True),
        sa.Column("area", sa.String(length=160), nullable=True),
        sa.Column("need_type", sa.String(length=60), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_leads_phone", "leads", ["phone"])
    op.create_index("ix_leads_status", "leads", ["status"])
    op.create_index("ix_leads_created_at", "leads", ["created_at"])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("action", sa.String(length=80), nullable=False),
        sa.Column("entity_table", sa.String(length=80), nullable=False),
        sa.Column("entity_id", sa.String(length=80), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])
    op.create_index("ix_audit_logs_entity_table", "audit_logs", ["entity_table"])
    op.create_index("ix_audit_logs_created_at", "audit_logs", ["created_at"])


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("leads")
    op.drop_table("vehicle_prices")
    op.drop_table("vehicle_variants")
    op.drop_table("vehicles")
