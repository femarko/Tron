import os
from typing import Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

from src.domain.errors import (
    ConfigError,
    ValidationError
)


class Settings(BaseSettings):

    mode: str = Field(..., validation_alias="MODE")
    host: str = Field(..., validation_alias="POSTGRES_HOST")
    port: int = Field(..., validation_alias="POSTGRES_PORT")
    user: str = Field(..., validation_alias="POSTGRES_USER")
    password: str = Field(..., validation_alias="POSTGRES_PASSWORD")
    db: str = Field(..., validation_alias="POSTGRES_DB")
    db_url: Optional[str] = Field(default=None)


    def model_post_init(self, __context: Any) -> None:
        try:
            self.db_url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        except AttributeError as e:
            raise ConfigError(message=f"Missing configuration variable when assembling DB URL: {e}") from e

    class Config:
        env_file = f".env.{os.getenv('MODE', 'prod')}"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    """
    Returns the application settings.

    Raises:
        ConfigError: If the settings could not be loaded.
    """
    try:
        # noinspection PyArgumentList
        return Settings()
    except ValidationError as e:
        raise ConfigError(str(e)) from e
