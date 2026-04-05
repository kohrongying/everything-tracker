from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_client_id: Optional[str] = Field(None, env="GOOGLE_CLIENT_ID")
    google_client_secret: Optional[str] = Field(None, env="GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = Field("http://localhost:8000/auth/callback", env="GOOGLE_REDIRECT_URI")
    dynamodb_table: str = Field("EverythingTracker", env="DYNAMODB_TABLE")
    aws_region: str = Field("ap-southeast-1", env="AWS_REGION")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
