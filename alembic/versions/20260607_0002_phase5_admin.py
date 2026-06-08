"""phase5 admin

Revision ID: 20260607_0002
Revises: 20260607_0001
Create Date: 2026-06-07
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260607_0002"
down_revision: str | None = "20260607_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("leads", sa.Column("admin_note", sa.Text(), nullable=True))
    op.add_column("leads", sa.Column("follow_up_at", sa.DateTime(), nullable=True))
    op.add_column("leads", sa.Column("last_contacted_at", sa.DateTime(), nullable=True))
    op.create_index("ix_leads_follow_up_at", "leads", ["follow_up_at"])

    op.add_column("vehicles", sa.Column("review_due_at", sa.Date(), nullable=True))
    op.create_index("ix_vehicles_review_due_at", "vehicles", ["review_due_at"])

    op.add_column("vehicle_prices", sa.Column("review_due_at", sa.Date(), nullable=True))
    op.create_index("ix_vehicle_prices_review_due_at", "vehicle_prices", ["review_due_at"])

    op.create_table(
        "content_items",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("kind", sa.String(length=40), nullable=False),
        sa.Column("title", sa.String(length=220), nullable=False),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("source_updated_at", sa.Date(), nullable=True),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column("review_due_at", sa.Date(), nullable=True),
        sa.Column("approval_status", sa.String(length=40), nullable=False),
        sa.Column("freshness_status", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_content_items_kind", "content_items", ["kind"])
    op.create_index("ix_content_items_approval_status", "content_items", ["approval_status"])
    op.create_index("ix_content_items_freshness_status", "content_items", ["freshness_status"])
    op.create_index("ix_content_items_review_due_at", "content_items", ["review_due_at"])


def downgrade() -> None:
    op.drop_table("content_items")
    op.drop_index("ix_vehicle_prices_review_due_at", table_name="vehicle_prices")
    op.drop_column("vehicle_prices", "review_due_at")
    op.drop_index("ix_vehicles_review_due_at", table_name="vehicles")
    op.drop_column("vehicles", "review_due_at")
    op.drop_index("ix_leads_follow_up_at", table_name="leads")
    op.drop_column("leads", "last_contacted_at")
    op.drop_column("leads", "follow_up_at")
    op.drop_column("leads", "admin_note")
