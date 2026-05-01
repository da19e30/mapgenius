"""Application configuration loaded from .env using pydantic BaseSettings.

All secrets must be stored in environment variables; .env is for local development only.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn, SecretStr

class Settings(BaseSettings):
    APP_NAME: str = "MapGenius SaaS"
    DEBUG: bool = False

    # JWT settings
    JWT_SECRET_KEY: SecretStr = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database URL (Postgres)
    DATABASE_URL: PostgresDsn = Field(..., env="DATABASE_URL")

    # Email (SMTP) – optional for dev
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: SecretStr | None = None
    EMAIL_FROM: str = "no-reply@mapgenius.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
