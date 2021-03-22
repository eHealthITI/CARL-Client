from typing import Optional
from pydantic import BaseSettings, Field, BaseModel


class AppConfig(BaseModel):
    """Application configurations."""

    NAME: str = "ypostirizoclient"


class GlobalConfig(BaseSettings):
    """Global configurations."""

    APP_CONFIG: AppConfig = AppConfig()
    CLOUD_URL: Optional[str] = Field(..., env='CLOUD_URL')
    CLOUD_TOKEN: Optional[str] = Field(..., env='CLOUD_TOKEN')
    # HC_TOKEN: Optional[str] = Field(..., env='HC_TOKEN')
    HC_PASSWORD: Optional[str] = Field(..., env='HC_PASSWORD')
    HC_USER: Optional[str] = Field(..., env='HC_USER')
    HC_URL: Optional[str] = Field(..., env='HC_URL')  # Never forget to include the protocol
    SUBJECT_ID: Optional[int] = Field(..., env='SUBJECT_ID')
    # CLOUD_USER: Optional[str] = Field(..., env='CLOUD_USER')
    DEBUG: Optional[bool] = Field(..., env='DEBUG')
    HC_INTERVAL: Optional[int] = Field(2, env='HC_DEVICES_INTERVAL')  # seconds
    CLOUD_DEVICES_INTERVAL: Optional[int] = Field(4, env='HC_DEVICES_INTERVAL')  # seconds
    CLOUD_EVENTS_INTERVAL: Optional[int] = Field(4, env='HC_EVENTS_INTERVAL')  # seconds

    class Config:
        """Loads the dotenv file."""
        env_file: str = ".env"


cnf = GlobalConfig()
