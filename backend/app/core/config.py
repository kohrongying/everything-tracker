from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Magic Link Auth Settings
    jwt_secret_key: str = Field("your-secret-key-change-in-production", validation_alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("HS256", validation_alias="JWT_ALGORITHM")
    magic_link_expiry_minutes: int = Field(15, validation_alias="MAGIC_LINK_EXPIRY_MINUTES")
    frontend_url: str = Field("http://localhost:3000", validation_alias="FRONTEND_URL")

    # AWS SES Settings
    ses_from_email: str = Field("noreply@yourdomain.com", validation_alias="SES_FROM_EMAIL")
    aws_region: str = Field("ap-southeast-1", validation_alias="AWS_REGION")

    # Database
    dynamodb_table: str = Field("EverythingTracker", validation_alias="DYNAMODB_TABLE")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
