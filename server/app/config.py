import os
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "MiniAppTG"
    DEBUG: bool = False
    DATABASE_URL: str

    SECRET_KEY: str
    BOT_TOKEN: str
    ALGORITHM: ClassVar[str] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    TELEGRAM_TOKEN_EXPIRATION: int = 86400

    # Comma-separated list in env (CORS_ORIGINS=https://a.com,https://b.com)
    CORS_ORIGINS_RAW: str = Field(
        default=(
            "http://localhost:5173,http://localhost:3000,"
            "http://127.0.0.1:5173,http://127.0.0.1:3000"
        ),
        alias="CORS_ORIGINS",
    )

    @property
    def CORS_ORIGINS(self) -> list[str]:
        return [item.strip() for item in self.CORS_ORIGINS_RAW.split(",") if item.strip()]

    def get_url_db(self) -> str:
        return self.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")

    base_dir: ClassVar[str] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_path: ClassVar[str] = os.path.join(base_dir, "static")
    images_path: ClassVar[str] = os.path.join(static_path, "images")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
