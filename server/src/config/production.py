from src.config import ConfigSettings
from pydantic_settings import SettingsConfigDict

class ProductionSettings(ConfigSettings):
    DEBUG: bool
    LOG_LEVEL: str
    
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file = (".env", ".env.production"),
        env_file_encoding = "utf-8",
        extra = "ignore"
    )

prod_settings: ProductionSettings = ProductionSettings() # type: ignore