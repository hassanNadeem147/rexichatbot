from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
class ModelSecretSettings(BaseSettings):
    """Secrets config for llm model"""
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )
    GOOGLE_API_KEY: str
    GOOGLE_MODEL: str
    TEMPERATURE: float
config_model = ModelSecretSettings()
class DatabaseSecretSettings(BaseSettings):
    """Secrets config for database"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}"
            f"/{self.DATABASE_NAME}"
        )
config_database = DatabaseSecretSettings()
class AuthSettings(BaseSettings):
    """Secrets and configuration for authentication."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
config_auth = AuthSettings()