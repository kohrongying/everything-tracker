import uuid

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.models.food import FoodCreate, FoodItem
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[FoodItem])
def get_food_entries(current_user: User = Depends(get_current_user)):
    # TODO: Load food entries from DynamoDB for the authenticated user
    return []

@router.post("/", response_model=FoodItem)
def add_food_entry(food: FoodCreate, current_user: User = Depends(get_current_user)):
    item = FoodItem(id=str(uuid.uuid4()), **food.model_dump())
    # TODO: Persist item to DynamoDB
    return item