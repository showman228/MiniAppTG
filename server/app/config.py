from pathlib import Path
from typing import Union, List, ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):

    BASE_DIR: ClassVar[Path] = Path(__file__).parent.parent.parent

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    SECRET_KEY: str

    APP_NAME: str = "STRL_SHOP"
    DEBUG: bool = True

    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    static_dir: str = "static"
    images_dir: str = "static/images"

    @property
    def get_url_db(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", extra="ignore"
    )


settings = Settings()
