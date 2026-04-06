from datetime import datetime, UTC
from pydantic import BaseModel, Field

class FocusSessionCreate(BaseModel):
    duration_seconds: int = Field(..., ge=1)
    started_at: datetime = Field(default_factory=datetime.now(UTC))

class FocusSessionItem(FocusSessionCreate):
    id: str
