from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ECHO_SQL: bool
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE: int
    REFRESH_TOKEN_EXPIRE: int
    REDIS_URL: str

    class Config:
        env_file = Path(__file__).parent / ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'


settings = Settings()
