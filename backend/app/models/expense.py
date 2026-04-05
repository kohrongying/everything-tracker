from datetime import date as Date
from typing import Optional
from pydantic import BaseModel, Field

class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Amount in SGD")
    description: str = Field(..., max_length=200)
    category: Optional[str] = Field(None, max_length=100)
    date: Date = Field(default_factory=lambda: Date.today())

class ExpenseItem(ExpenseCreate):
    id: str
