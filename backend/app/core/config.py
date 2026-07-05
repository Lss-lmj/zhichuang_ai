from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="智创Agent", alias="APP_NAME")
    app_env: str = Field(default="dev", alias="APP_ENV")
    api_prefix: str = Field(default="/api", alias="API_PREFIX")
    database_url: str = Field(default="sqlite:///./data/local/app.db", alias="DATABASE_URL")
    vector_store: str = Field(default="chroma", alias="VECTOR_STORE")
    vector_store_path: str = Field(default="./data/local/chroma", alias="VECTOR_STORE_PATH")
    storage_root: str = Field(default="./data/local/uploads", alias="STORAGE_ROOT")
    llm_provider: str = Field(default="mock", alias="LLM_PROVIDER")
    embedding_provider: str = Field(default="mock", alias="EMBEDDING_PROVIDER")
    jwt_secret: str = Field(default="dev-secret", alias="JWT_SECRET")
    school_identity_shared_secret: str = Field(
        default="dev-school-identity-secret",
        alias="SCHOOL_IDENTITY_SHARED_SECRET",
    )
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
