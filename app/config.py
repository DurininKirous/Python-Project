from functools import lru_cache
from typing import Annotated

from pydantic import BaseSettings, Field, UrlConstraints

DatabaseDsn = Annotated[
    str,
    UrlConstraints(
        schemes={"postgresql", "postgresql+asyncpg", "sqlite+aiosqlite"},
    ),
]


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = Field("learning-fastapi", env="APP_NAME")
    database_url: DatabaseDsn = Field(
        "postgresql+asyncpg://postgres:postgres@db:5432/app",
        env="DATABASE_URL",
    )
    prometheus_metrics_path: str = Field("/metrics", env="PROMETHEUS_METRICS_PATH")
    log_level: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
