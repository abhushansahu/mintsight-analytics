from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/db"
    database_url_sync: str = "postgresql://user:pass@localhost:5432/db"
    helius_api_key: str = ""
    helius_webhook_secret: str = ""
    api_key: str = ""
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
