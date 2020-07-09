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
    HC_TOKEN: Optional[str] = Field(None, env='HC_TOKEN')
    HC_USER: Optional[str] = Field(None, env='HC_USER')
    SUBJECT_ID: Optional[int] = Field(None, env='SUBJECT_ID')
    CLOUD_USER: Optional[str] = Field(None, env='CLOUD_USER')
    DEBUG: Optional[bool] = Field(False, env='DEBUG')

    class Config:
        """Loads the dotenv file."""
        env_file: str = ".env"


cnf = GlobalConfig()
