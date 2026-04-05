import uuid

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.models.focus import FocusSessionCreate, FocusSessionItem
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[FocusSessionItem])
def get_focus_sessions(current_user: User = Depends(get_current_user)):
    # TODO: Load focus sessions from DynamoDB for the authenticated user
    return []

@router.post("/", response_model=FocusSessionItem)
def start_focus_session(focus: FocusSessionCreate, current_user: User = Depends(get_current_user)):
    item = FocusSessionItem(id=str(uuid.uuid4()), **focus.model_dump())
    # TODO: Persist item to DynamoDB
    return item