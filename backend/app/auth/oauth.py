import boto3
import logging
import secrets
from datetime import datetime, timedelta, UTC
from typing import Optional

from jose import JWTError, jwt

from app.core.config import settings

logger = logging.getLogger("everything-tracker.auth")

def _get_ses_client():
    """Lazy initialization of SES client to avoid credential issues at import time."""
    return boto3.client('ses', region_name=settings.aws_region)

def generate_magic_link_token(email: str) -> str:
    """Generate a secure JWT token for magic link authentication."""
    expire = datetime.now(UTC) + timedelta(minutes=settings.magic_link_expiry_minutes)
    to_encode = {
        "email": email,
        "exp": expire,
        "type": "magic_link",
        "jti": secrets.token_urlsafe(32)  # Unique token ID for one-time use
    }
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_magic_link_token(token: str) -> Optional[str]:
    """Verify and decode magic link token. Returns email if valid, None if invalid."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        email: str = payload.get("email")
        token_type: str = payload.get("type")

        if token_type != "magic_link":
            logger.warning(
                "Invalid token type for magic link verification",
                extra={
                    "extra_fields": {
                        "event": "token_verification_failed",
                        "reason": "invalid_token_type",
                        "token_type": token_type,
                    }
                }
            )
            return None

        logger.info(
            "Magic link token verified successfully",
            extra={
                "extra_fields": {
                    "email": email,
                    "event": "magic_link_token_verified",
                }
            }
        )

        return email
    except JWTError as e:
        logger.warning(
            "JWT verification failed for magic link token",
            extra={
                "extra_fields": {
                    "event": "token_verification_failed",
                    "reason": "jwt_error",
                    "error": str(e),
                }
            }
        )
        return None

def send_magic_link_email(email: str) -> bool:
    """Send magic link email using AWS SES."""
    try:
        logger.info(
            "Sending magic link email",
            extra={
                "extra_fields": {
                    "email": email,
                    "event": "email_send_attempt",
                }
            }
        )

        ses_client = _get_ses_client()
        token = generate_magic_link_token(email)
        magic_link = f"{settings.frontend_url}/auth/verify?token={token}"

        subject = "Login to Everything Tracker"
        body_text = f"""
        Welcome to Everything Tracker!

        Click the link below to sign in to your account:

        {magic_link}

        This link will expire in {settings.magic_link_expiry_minutes} minutes.

        If you didn't request this link, please ignore this email.

        Best regards,
        Everything Tracker Team
        """

        body_html = f"""
        <html>
        <head></head>
        <body>
            <h2>Welcome to Everything Tracker!</h2>
            <p>Click the button below to sign in to your account:</p>
            <p>
                <a href="{magic_link}" style="background-color: #4CAF50; color: white; padding: 14px 20px; text-decoration: none; border-radius: 4px; display: inline-block;">
                    Sign In to Everything Tracker
                </a>
            </p>
            <p><small>This link will expire in {settings.magic_link_expiry_minutes} minutes.</small></p>
            <p><small>If you didn't request this link, please ignore this email.</small></p>
            <br>
            <p>Best regards,<br>Everything Tracker Team</p>
        </body>
        </html>
        """

        response = ses_client.send_email(
            Source=settings.ses_from_email,
            Destination={
                'ToAddresses': [email]
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body_text,
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': body_html,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )

        logger.info(
            "Magic link email sent successfully",
            extra={
                "extra_fields": {
                    "email": email,
                    "event": "email_sent",
                    "message_id": response.get('MessageId'),
                }
            }
        )

        return True

    except Exception as e:
        logger.error(
            "Failed to send magic link email",
            exc_info=True,
            extra={
                "extra_fields": {
                    "email": email,
                    "event": "email_send_error",
                    "error": str(e),
                }
            }
        )
        return False

def generate_access_token(user_uuid: str) -> str:
    """Generate a JWT access token for authenticated users."""
    expire = datetime.now(UTC) + timedelta(days=7)  # 7 days expiry
    to_encode = {
        "user_uuid": user_uuid,
        "exp": expire,
        "type": "access_token"
    }
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_access_token(token: str) -> Optional[str]:
    """Verify and decode access token. Returns (user_uuid) if valid, None if invalid."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_uuid: str = payload.get("user_uuid")
        token_type: str = payload.get("type")

        if token_type != "access_token":
            logger.warning(
                "Invalid token type for access token verification",
                extra={
                    "extra_fields": {
                        "event": "access_token_verification_failed",
                        "reason": "invalid_token_type",
                        "token_type": token_type,
                    }
                }
            )
            return None

        return user_uuid
    except JWTError as e:
        logger.warning(
            "JWT verification failed for access token",
            extra={
                "extra_fields": {
                    "event": "access_token_verification_failed",
                    "reason": "jwt_error",
                    "error": str(e),
                }
            }
        )
        return None
