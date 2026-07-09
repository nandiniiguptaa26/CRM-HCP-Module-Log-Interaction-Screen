from pydantic import BaseModel
from typing import Optional


class InteractionCreate(BaseModel):

    hcp_name: str

    meeting_type: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: Optional[str] = None
    discussion: Optional[str] = None

    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None

    summary: Optional[str] = None
    follow_up: Optional[str] = None
    materials_shared: str | None = ""

    samples_distributed: str | None = ""

    sentiment: str | None = ""

    outcomes: str | None = ""

    follow_up_actions: str | None = ""


class InteractionResponse(InteractionCreate):

    id: int

    class Config:
        from_attributes = True