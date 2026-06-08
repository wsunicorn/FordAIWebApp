from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Lead
from app.schemas import LeadCreate
from app.services.audit_service import write_audit_log


async def create_lead(session: AsyncSession, lead_in: LeadCreate) -> Lead:
    lead = Lead(**lead_in.model_dump())
    session.add(lead)
    await session.commit()
    await session.refresh(lead)
    await write_audit_log(
        session,
        action="lead.created",
        entity_table="leads",
        entity_id=lead.id,
        metadata={"need_type": lead.need_type, "vehicle_interest": lead.vehicle_interest},
    )
    await write_audit_log(
        session,
        action="notification.pending",
        entity_table="leads",
        entity_id=lead.id,
        metadata={
            "channels": ["admin", "email", "zalo", "sheets"],
            "reason": "new_lead",
            "need_type": lead.need_type,
        },
    )
    return lead
