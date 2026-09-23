from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Rijeka Transit API"
    app_version: str = "0.1.0"

    autotrolej_base_url: str = "https://api.autotrolej.hr/api/open/v1"
    autotrolej_username: str = ""
    autotrolej_password: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
