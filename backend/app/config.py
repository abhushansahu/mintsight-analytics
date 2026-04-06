from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://onchain_spade:spade_dev_pass@localhost:5432/onchain_spade"
    database_url_sync: str = "postgresql://onchain_spade:spade_dev_pass@localhost:5432/onchain_spade"
    helius_api_key: str = ""
    helius_webhook_secret: str = ""
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
