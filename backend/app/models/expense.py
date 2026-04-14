from datetime import date, datetime
from pydantic import BaseModel, Field
from decimal import Decimal

class ExpenseCreate(BaseModel):
    amount: str = Field(...)
    description: str = Field(..., max_length=200)
    category: str = Field(..., max_length=50)
    expense_date: datetime = Field(default_factory=lambda: date.today())

class ExpenseItem(BaseModel):
    id: str
    user_id: str
    amount: Decimal
    description: str
    category: str
    expense_date: datetime
