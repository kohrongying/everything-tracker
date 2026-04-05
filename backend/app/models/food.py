from datetime import date as Date
from pydantic import BaseModel, Field

class FoodCreate(BaseModel):
    name: str = Field(..., max_length=200)
    calories: int = Field(..., ge=0)
    protein: int = Field(..., ge=0)
    date: Date = Field(default_factory=lambda: Date.today())

class FoodItem(FoodCreate):
    id: str
