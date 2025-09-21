from functools import lru_cache
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    type: str = Field(default="sqlite", description="Database type (sqlite, postgresql)")
    url: Optional[str] = Field(default=None, description="Complete database URL")
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    database: str = Field(default="pipeline_db", description="Database name")
    user: str = Field(default="pipeline_user", description="Database user")
    password: str = Field(default="pipeline_password", description="Database password")

    def get_url(self) -> str:
        if self.url:
            return self.url
        
        if self.type == "sqlite":
            return "sqlite:///data/pipeline.db"
        elif self.type == "postgresql":
            return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        else:
            raise ValueError(f"Unsupported database type: {self.type}")


class APISettings(BaseSettings):
    base_url: str = Field(
        default="https://jsonplaceholder.typicode.com",
        description="Base URL for the API"
    )
    timeout: int = Field(default=30, description="Request timeout in seconds")
    retries: int = Field(default=3, description="Number of retries")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__"
    )

    environment: str = Field(default="development", description="Environment")
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    log_level: str = Field(default="INFO", description="Log level")
    data_dir: str = Field(default="data", description="Data directory")
    reports_dir: str = Field(default="reports", description="Reports directory")

    # Database settings
    database_url: Optional[str] = Field(default=None, description="Database URL")
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default="pipeline_db")
    postgres_user: str = Field(default="pipeline_user")
    postgres_password: str = Field(default="pipeline_password")

    @property
    def database(self) -> DatabaseSettings:
        if self.database_url:
            if self.database_url.startswith("sqlite"):
                return DatabaseSettings(type="sqlite", url=self.database_url)
            elif self.database_url.startswith("postgresql"):
                return DatabaseSettings(type="postgresql", url=self.database_url)
        
        # Default to PostgreSQL in production, SQLite in development
        if self.environment == "production":
            return DatabaseSettings(
                type="postgresql",
                host=self.postgres_host,
                port=self.postgres_port,
                database=self.postgres_db,
                user=self.postgres_user,
                password=self.postgres_password
            )
        else:
            return DatabaseSettings(type="sqlite", url="sqlite:///data/pipeline.db")

    @property
    def api(self) -> APISettings:
        return APISettings()


@lru_cache()
def get_settings() -> Settings:
    return Settings()