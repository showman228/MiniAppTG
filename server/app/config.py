import os
from typing import ClassVar

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "MiniAppTG"
    DEBUG: bool = True  # ВЫКЛЮЧИТЬ НАХУЙ ПРИ ПРОДАКШЕНЕ
    DATABASE_URL: str = Field(default="postgresql+asyncpg://postgres:postgres@db:5432/mini_app_db", env="DATABASE_URL")

    SECRET_KEY: ClassVar[str] = os.getenv("SECRET_KEY")
    BOT_TOKEN: ClassVar[str] = os.getenv("BOT_TOKEN")
    ALGORITHM: ClassVar[str] = "HS256"
    TOKEN_EXPIRATION: int = 60 * 24 # токен действителен 24 часа, потом он обновляется

    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

    # вопрос, как сделать так, чтобы это все работало в докере????
    base_dir: ClassVar[str] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_path: ClassVar[str] = os.path.join(base_dir, "static")
    images_path: ClassVar[str] = os.path.join(static_path, "images")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()