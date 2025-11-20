"""
Application-wide configuration using pydantic-settings.

This lets us drive the framework via environment variables or a .env file:
- BASE_URL: API base URL (e.g. http://localhost:8080)
- UI_URL:   UI base URL (e.g. http://localhost:3000)
- AUTH_TOKEN: optional bearer token for authenticated API tests
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Strongly-typed configuration for tests."""
    env: str = "local"
    base_url: str = "http://localhost:8080"
    ui_url: str = "http://localhost:3000"
    auth_token: str | None = None
    api_timeout: int = 10

    class Config:
        # Allow direct ENV names (BASE_URL, UI_URL, etc.)
        env_prefix = ""
        env_file = ".env"
        extra = "ignore"


settings = Settings()
