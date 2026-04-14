import logging
from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.models.expense import ExpenseCreate, ExpenseItem
from app.models.user import User
from app.services.dynamodb import get_user_expenses, add_expense as db_add_expense

router = APIRouter()
logger = logging.getLogger("everything-tracker.expense")

@router.get("/", response_model=list[ExpenseItem])
def get_expenses(current_user: User = Depends(get_current_user)):
    logger.info(
        "Fetching expenses",
        extra={
            "extra_fields": {
                "user_id": current_user.uuid,
                "event": "expenses_fetch_requested",
            }
        }
    )
    expenses = get_user_expenses(current_user.uuid)
    return expenses

@router.post("/", response_model=ExpenseItem)
def add_expense(expense: ExpenseCreate, current_user: User = Depends(get_current_user)):
    logger.info(
        "Adding expense",
        extra={
            "extra_fields": {
                "user_id": current_user.uuid,
                "amount": expense.amount,
                "event": "expense_creation_requested",
            }
        }
    )
    # Override user_id with current authenticated user's uuid for security
    item = db_add_expense(
        user_id=current_user.uuid,
        amount=expense.amount,
        description=expense.description,
        category=expense.category,
        expense_date=expense.expense_date.isoformat(),
    )
    logger.info(
        "Expense added successfully",
        extra={
            "extra_fields": {
                "user_id": current_user.uuid,
                "expense_id": item.id,
                "amount": expense.amount,
                "event": "expense_created",
            }
        }
    )
    return item