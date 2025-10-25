from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Agent CRUD API"
    database_url: str = "sqlite+aiosqlite:///./app.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()
