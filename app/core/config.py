from typing import Optional

from pydantic import BaseSettings, EmailStr

DEFAULT_AMOUNT = 0
MAX_LENGTH = 100


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
