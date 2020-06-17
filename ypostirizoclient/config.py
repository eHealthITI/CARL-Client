from typing import Optional
from pydantic import BaseSettings, Field, BaseModel


class AppConfig(BaseModel):
    """Application configurations."""

    NAME: str = "ypostirizoclient"


class GlobalConfig(BaseSettings):
    """Global configurations."""

    APP_CONFIG: AppConfig = AppConfig()
    CLOUD_URL: Optional[str] = Field(None, env='CLOUD_URL')
    CLOUD_TOKEN: Optional[str] = Field(None, env='CLOUD_TOKEN')
    SUBJECT_ID: Optional[int] = Field(None, env='SUBJECT_ID')
    USER_ID: Optional[str] = Field(None, env='CLOUD_USER')
    DEBUG: Optional[bool] = Field(False, env='DEBUG')

    class Config:
        """Loads the dotenv file."""
        env_file: str = ".env"


cnf = GlobalConfig()