from urllib.parse import urlencode

from app.core.config import settings

GOOGLE_AUTH_BASE = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def get_google_auth_url() -> str:
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    return f"{GOOGLE_AUTH_BASE}?{urlencode(params)}"


def exchange_code_for_token(code: str) -> dict:
    # TODO: Exchange the authorization code for tokens using Google OAuth.
    return {
        "access_token": "TODO",
        "id_token": "TODO"
    }


def get_user_info(access_token: str) -> dict:
    # TODO: Use Google userinfo endpoint to get profile details.
    return {
        "email": "user@example.com",
        "name": "Example User",
        "sub": "1234567890"
    }
