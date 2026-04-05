from datetime import date as Date
from pydantic import BaseModel, Field

class ExerciseCreate(BaseModel):
    name: str = Field(..., max_length=200)
    weight: float = Field(..., ge=0)
    reps: int = Field(..., ge=0)
    sets: int = Field(..., ge=0)
    date: Date = Field(default_factory=lambda: Date.today())

class ExerciseItem(ExerciseCreate):
    id: str
