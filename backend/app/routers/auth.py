import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.auth.dependencies import get_current_user
from app.auth.oauth import send_magic_link_email, verify_magic_link_token, generate_access_token
from app.models.user import User

router = APIRouter()
logger = logging.getLogger("everything-tracker.auth")

class MagicLinkRequest(BaseModel):
    email: EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/magic-link", status_code=status.HTTP_200_OK)
def request_magic_link(request: MagicLinkRequest):
    """Request a magic link to be sent to the provided email address."""
    logger.info(
        "Magic link requested",
        extra={
            "extra_fields": {
                "email": request.email,
                "event": "magic_link_requested",
            }
        }
    )

    success = send_magic_link_email(request.email)
    if not success:
        logger.error(
            "Failed to send magic link email",
            extra={
                "extra_fields": {
                    "email": request.email,
                    "event": "magic_link_send_failed",
                }
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send magic link email"
        )

    logger.info(
        "Magic link sent successfully",
        extra={
            "extra_fields": {
                "email": request.email,
                "event": "magic_link_sent",
            }
        }
    )

    return {"message": "Magic link sent successfully. Check your email."}

@router.get("/verify", response_model=TokenResponse)
def verify_magic_link(token: str):
    """Verify magic link token and return access token."""
    logger.info(
        "Magic link verification attempted",
        extra={
            "extra_fields": {
                "event": "magic_link_verification_attempted",
            }
        }
    )

    email = verify_magic_link_token(token)
    if not email:
        logger.warning(
            "Invalid or expired magic link token",
            extra={
                "extra_fields": {
                    "event": "magic_link_verification_failed",
                    "reason": "invalid_or_expired_token",
                }
            }
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired magic link"
        )

    access_token = generate_access_token(email)

    logger.info(
        "Magic link verified successfully",
        extra={
            "extra_fields": {
                "email": email,
                "event": "magic_link_verified",
            }
        }
    )

    return TokenResponse(access_token=access_token)

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    logger.info(
        "User profile accessed",
        extra={
            "extra_fields": {
                "email": current_user.email,
                "event": "user_profile_accessed",
            }
        }
    )
    return current_user
