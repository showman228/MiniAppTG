import os
from typing import ClassVar

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "MiniAppTG"
    DEBUG: bool = True  # ВЫКЛЮЧИТЬ НАХУЙ ПРИ ПРОДАКШЕНЕ
    DATABASE_URL: str = Field(default="postgresql+asyncpg://postgres:postgres@db:5432/mini_app_db", env="DATABASE_URL")

    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")
    ALGORITHM: ClassVar[str] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # токен действителен 24 часа, потом он обновляется
    TELEGRAM_TOKEN_EXPIRATION: int = 86400

    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

    base_dir: ClassVar[str] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_path: ClassVar[str] = os.path.join(base_dir, "static")
    images_path: ClassVar[str] = os.path.join(static_path, "images")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()