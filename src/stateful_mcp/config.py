from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str

    # Server
    server_host: str = Field(default="127.0.0.1")
    server_port: int = Field(default=8000)

    # App
    app_env: Literal["dev", "staging", "prod"] = Field(default="dev")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO")


settings = Settings()