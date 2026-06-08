from pydantic import BaseModel, Field


class AIChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=1200)
    session_id: str | None = Field(default=None, max_length=80)
    vehicle_interest: str | None = Field(default=None, max_length=160)


class AISourceRead(BaseModel):
    id: str
    title: str
    source_url: str | None = None
    source_updated_at: str | None = None


class AIChatResponse(BaseModel):
    conversation_id: str
    session_id: str
    message_id: str
    answer: str
    sources: list[AISourceRead]
    risk_flags: list[str]
    handoff_required: bool
    provider_name: str | None = None
    tool_name: str | None = None
    fallback_used: bool = False


class AIHandoffRequest(BaseModel):
    conversation_id: str
    full_name: str = Field(min_length=2, max_length=160)
    phone: str = Field(min_length=8, max_length=40)
    vehicle_interest: str | None = Field(default=None, max_length=160)
    area: str | None = Field(default=None, max_length=160)
    note: str | None = Field(default=None, max_length=2000)


class AIHandoffResponse(BaseModel):
    ok: bool
    lead_id: str


class AIFeedbackRequest(BaseModel):
    message_id: str
    rating: int = Field(ge=-1, le=1)
    note: str | None = Field(default=None, max_length=1000)
