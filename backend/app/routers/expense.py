import uuid

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.models.expense import ExpenseCreate, ExpenseItem
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[ExpenseItem])
def get_expenses(current_user: User = Depends(get_current_user)):
    # TODO: Load expense items from DynamoDB for the authenticated user
    return []

@router.post("/", response_model=ExpenseItem)
def add_expense(expense: ExpenseCreate, current_user: User = Depends(get_current_user)):
    item = ExpenseItem(id=str(uuid.uuid4()), **expense.model_dump())
    # TODO: Persist item to DynamoDB
    return item