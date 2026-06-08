from datetime import datetime

from pydantic import BaseModel, Field


class LeadCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=160)
    phone: str = Field(min_length=8, max_length=40)
    vehicle_interest: str | None = Field(default=None, max_length=160)
    area: str | None = Field(default=None, max_length=160)
    need_type: str = Field(default="quote", max_length=60)
    note: str | None = Field(default=None, max_length=2000)


class LeadRead(LeadCreate):
    id: str
    status: str
    created_at: datetime
