from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = "StockSage India"
    app_env: str = "development"
    app_port: int = 8000
    log_level: str = "INFO"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    redis_ttl_price: int = 3600
    redis_ttl_news: int = 1800

    # Stock data defaults
    default_exchange: str = "NS"
    default_period: str = "1y"
    default_interval: str = "1d"

    # News APIs
    newsapi_key: str = ""

    # GenAI
    anthropic_api_key: str = ""


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()