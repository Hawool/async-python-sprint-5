import os
from logging import config as logging_config

from pydantic import BaseSettings, PostgresDsn

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

    DATABASE_DSN: PostgresDsn = 'postgresql+asyncpg://postgres:postgres@localhost:5555/postgres'

    FILE_FOLDER: str = 'files/'

    class Config:
        env_file = '../.env', '.env'


app_settings = AppSettings()
