from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    DATABASE_URL: str
    TELEGRAM_INIT_DATA_MAX_AGE_SECONDS: int = 86_400
    ALLOW_DEV_AUTH: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
