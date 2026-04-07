import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from aws_lambda_powertools.utilities import parameters


def _is_deployed() -> bool:
    return bool(os.getenv("AWS_LAMBDA_FUNCTION_NAME"))


def _get_parameter_if_deployed(name: str, default: str, decrypt: bool = False) -> str:
    if _is_deployed() and name:
        try:
            return parameters.get_parameter(name, decrypt=decrypt, max_age=3600)
        except Exception:
            return default
    return default


class Settings(BaseSettings):
    # Magic Link Auth Settings
    jwt_secret_key_param_name: str = Field("", validation_alias="JWT_SECRET_KEY_PARAMETER_NAME")
    jwt_secret_key: str = Field("your-secret-key-change-in-production", validation_alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("HS256", validation_alias="JWT_ALGORITHM")
    magic_link_expiry_minutes: int = Field(15, validation_alias="MAGIC_LINK_EXPIRY_MINUTES")

    frontend_url_param_name: str = Field("", validation_alias="FRONTEND_URL_PARAMETER_NAME")
    frontend_url: str = Field("http://localhost:3000", validation_alias="FRONTEND_URL")

    # AWS SES Settings
    ses_from_email: str = Field("noreply@yourdomain.com", validation_alias="SES_FROM_EMAIL")
    aws_region: str = Field("ap-southeast-1", validation_alias="AWS_REGION")

    # Database
    dynamodb_table: str = Field("EverythingTracker", validation_alias="DYNAMODB_TABLE")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def __init__(self, **values):
        super().__init__(**values)

        self.jwt_secret_key = _get_parameter_if_deployed(
            self.jwt_secret_key_param_name,
            self.jwt_secret_key,
            decrypt=True,
        )

        self.frontend_url = _get_parameter_if_deployed(
            self.frontend_url_param_name,
            self.frontend_url,
        )


settings = Settings()
