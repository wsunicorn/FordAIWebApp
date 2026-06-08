"""phase6 ai assistant

Revision ID: 20260607_0003
Revises: 20260607_0002
Create Date: 2026-06-07
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260607_0003"
down_revision: str | None = "20260607_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ai_documents",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=220), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("source_updated_at", sa.Date(), nullable=True),
        sa.Column("owner", sa.String(length=120), nullable=False),
        sa.Column("approval_status", sa.String(length=40), nullable=False),
        sa.Column("freshness_status", sa.String(length=40), nullable=False),
        sa.Column("risk_level", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_ai_documents_approval_status", "ai_documents", ["approval_status"])
    op.create_index("ix_ai_documents_freshness_status", "ai_documents", ["freshness_status"])
    op.create_index("ix_ai_documents_risk_level", "ai_documents", ["risk_level"])

    op.create_table(
        "ai_conversations",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("session_id", sa.String(length=80), nullable=False),
        sa.Column("customer_name", sa.String(length=160), nullable=True),
        sa.Column("phone", sa.String(length=40), nullable=True),
        sa.Column("vehicle_interest", sa.String(length=160), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_ai_conversations_session_id", "ai_conversations", ["session_id"])
    op.create_index("ix_ai_conversations_phone", "ai_conversations", ["phone"])
    op.create_index("ix_ai_conversations_status", "ai_conversations", ["status"])
    op.create_index("ix_ai_conversations_created_at", "ai_conversations", ["created_at"])

    op.create_table(
        "ai_messages",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "conversation_id",
            sa.String(length=36),
            sa.ForeignKey("ai_conversations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("role", sa.String(length=24), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("source_ids", sa.Text(), nullable=True),
        sa.Column("tool_name", sa.String(length=80), nullable=True),
        sa.Column("risk_flags", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_ai_messages_conversation_id", "ai_messages", ["conversation_id"])
    op.create_index("ix_ai_messages_role", "ai_messages", ["role"])
    op.create_index("ix_ai_messages_created_at", "ai_messages", ["created_at"])

    op.create_table(
        "ai_feedback",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "message_id",
            sa.String(length=36),
            sa.ForeignKey("ai_messages.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_ai_feedback_message_id", "ai_feedback", ["message_id"])
    op.create_index("ix_ai_feedback_created_at", "ai_feedback", ["created_at"])


def downgrade() -> None:
    op.drop_table("ai_feedback")
    op.drop_table("ai_messages")
    op.drop_table("ai_conversations")
    op.drop_table("ai_documents")
