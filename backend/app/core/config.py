import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from aws_lambda_powertools.utilities import parameters


def _is_production() -> bool:
    return os.getenv("STAGE") == "prod"


def _get_parameter(name: str, default: str, decrypt: bool = False) -> str:
    try:
        return parameters.get_parameter(name, decrypt=decrypt, max_age=3600)
    except Exception:
        return default


class Settings(BaseSettings):
    # Magic Link Auth Settings
    jwt_secret_key_param_name: str = Field(
        "", validation_alias="JWT_SECRET_KEY_PARAMETER_NAME"
    )
    jwt_secret_key: str = Field(
        "your-secret-key-change-in-production", validation_alias="JWT_SECRET_KEY"
    )
    jwt_algorithm: str = Field("HS256", validation_alias="JWT_ALGORITHM")
    magic_link_expiry_minutes: int = Field(
        15, validation_alias="MAGIC_LINK_EXPIRY_MINUTES"
    )

    # Netlify URL
    frontend_url: str = Field("http://localhost:3000", validation_alias="FRONTEND_URL")

    # AWS SES Settings
    ses_from_email: str = Field(
        "noreply@yourdomain.com", validation_alias="SES_FROM_EMAIL"
    )
    aws_region: str = Field("ap-southeast-1", validation_alias="AWS_REGION")

    # DynamoDB Tables
    users_table_name: str = Field(
        "everything-tracker-users", validation_alias="USERS_TABLE_NAME"
    )
    expenses_table_name: str = Field(
        "everything-tracker-expenses", validation_alias="EXPENSES_TABLE_NAME"
    )

    # Local DynamoDB Configuration
    use_local_dynamodb: bool = Field(False, validation_alias="USE_LOCAL_DYNAMODB")
    local_dynamodb_endpoint: str = Field(
        "http://localhost:8000", validation_alias="LOCAL_DYNAMODB_ENDPOINT"
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def __init__(self, **values):
        super().__init__(**values)

        # Set local DynamoDB based on environment
        if _is_production():
            self.jwt_secret_key = _get_parameter(
                self.jwt_secret_key_param_name,
                self.jwt_secret_key,
                decrypt=True,
            )

settings = Settings()
