import os
from logging import config as logging_config
from typing import Any, Optional

from pydantic import BaseSettings, PostgresDsn, validator

from src.core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppSettings(BaseSettings):
    APP_TITLE: str = "File Storage"
    HOST: str = '0.0.0.0'
    PORT: int = 9000
    SECRET: str = 'secret'

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    DATABASE_DSN: Optional[PostgresDsn] = None

    @validator("DATABASE_DSN", pre=True)
    def assemble_db_connection(cls, value: Optional[str], values: dict[str, Any]) -> Any:  # type: ignore
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    FILE_FOLDER: str = 'files'
    MAX_FILE_SIZE: int = 1024 * 1024  # 1 Mb

    class Config:
        env_file = '../.env', '.env'


app_settings = AppSettings()
