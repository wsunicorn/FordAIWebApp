from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_session
from app.schemas import (
    AIChatRequest,
    AIChatResponse,
    AIFeedbackRequest,
    AIHandoffRequest,
    AIHandoffResponse,
    LeadCreate,
    LeadRead,
)
from app.services.ai_service import (
    answer_chat,
    create_ai_feedback,
    handoff_conversation_to_lead,
)
from app.services.audit_service import write_audit_log
from app.services.lead_service import create_lead

router = APIRouter(tags=["api"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


class RevalidateRequest(BaseModel):
    secret: str
    paths: list[str] = []
    tags: list[str] = []
    reason: str = "manual"


@router.get("/health")
async def health():
    return {
        "ok": True,
        "service": "ford-ai-webapp",
        "stack": "fastapi-jinja-tailwind",
        "environment": settings.app_env,
    }


@router.get("/health/db")
async def health_db(session: SessionDep):
    await session.execute(text("SELECT 1"))
    return {"ok": True, "database": "reachable"}


@router.post("/leads", response_model=LeadRead)
async def create_lead_api(lead_in: LeadCreate, session: SessionDep):
    lead = await create_lead(session, lead_in)
    return lead


@router.post("/ai/chat", response_model=AIChatResponse)
async def ai_chat(payload: AIChatRequest, session: SessionDep):
    return await answer_chat(session, payload)


@router.post("/ai/handoff", response_model=AIHandoffResponse)
async def ai_handoff(payload: AIHandoffRequest, session: SessionDep):
    lead = await handoff_conversation_to_lead(
        session,
        conversation_id=payload.conversation_id,
        full_name=payload.full_name,
        phone=payload.phone,
        vehicle_interest=payload.vehicle_interest,
        area=payload.area,
        note=payload.note,
    )
    if not lead:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return AIHandoffResponse(ok=True, lead_id=lead.id)


@router.post("/ai/feedback")
async def ai_feedback(payload: AIFeedbackRequest, session: SessionDep):
    feedback = await create_ai_feedback(
        session,
        message_id=payload.message_id,
        rating=payload.rating,
        note=payload.note,
    )
    if not feedback:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"ok": True}


@router.post("/revalidate")
async def revalidate(payload: RevalidateRequest, session: SessionDep):
    if payload.secret != settings.revalidation_secret:
        raise HTTPException(status_code=401, detail="Unauthorized")

    await write_audit_log(
        session,
        action="cache.revalidate",
        entity_table="cache",
        metadata={"paths": payload.paths, "tags": payload.tags, "reason": payload.reason},
    )

    return {"ok": True, "paths": payload.paths, "tags": payload.tags}
