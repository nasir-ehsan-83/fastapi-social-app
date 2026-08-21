from src.config import ConfigSettings
from pydantic_settings import SettingsConfigDict

class DevelopmentSettings(ConfigSettings):
    DEBUG: bool
    LOG_LEVEL: str
    
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file = (".env", ".env.development"),
        env_file_encoding = "utf-8",
        extra = "ignore"
    )

dev_settings: DevelopmentSettings = DevelopmentSettings() # type: ignore
