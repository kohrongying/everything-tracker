import uuid

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.models.exercise import ExerciseCreate, ExerciseItem
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[ExerciseItem])
def get_exercises(current_user: User = Depends(get_current_user)):
    # TODO: Load exercise entries from DynamoDB for the authenticated user
    return []

@router.post("/", response_model=ExerciseItem)
def add_exercise(exercise: ExerciseCreate, current_user: User = Depends(get_current_user)):
    item = ExerciseItem(id=str(uuid.uuid4()), **exercise.model_dump())
    # TODO: Persist item to DynamoDB
    return item