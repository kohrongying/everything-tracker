from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from typing import Optional

from app.auth.dependencies import get_current_user
from app.auth.oauth import get_google_auth_url
from app.models.user import User

router = APIRouter()

@router.get("/login")
def login():
    return RedirectResponse(get_google_auth_url())

@router.get("/callback")
def callback(code: Optional[str] = None):
    if code is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing authorization code")

    return {"message": "OAuth callback received", "code": code}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user