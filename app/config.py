from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = Field(default="OddsEngine")
    app_env: Literal["local", "development", "testing", "production"] = Field(default="local")
    app_debug: bool = Field(default=True)
    app_version: str = Field(default="0.1.0")
    api_v1_prefix: str = Field(default="/api/v1")

    database_url: str = Field(
        default="postgresql+asyncpg://odds_engine:odds_engine@localhost:5432/odds_engine"
    )
    redis_url: str = Field(default="redis://localhost:6379/0")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()