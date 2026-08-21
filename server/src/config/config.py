from typing import List
from pydantic_settings import (
    BaseSettings, 
    SettingsConfigDict
)

class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    
    REDIS_HOST: str
    REDIS_PORT: int
    
    ACCESS_TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    REFRESH_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_DAYS: int 

    ALGORITHM: str

    DEBUG: bool 
    ALLOWED_HOSTS: List[str] 
    LOG_LEVEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings: Settings = Settings() # type: ignore
