from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Enrich Investments Backend"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:8080",
            "http://localhost:5173",
            "https://vinehps.github.io",
        ]
    )

    # Database
    MONGODB_URL: str
    DATABASE_NAME: str = "enrich_investments"

    # Security
    SECRET_KEY: str  # Used for Fernet encryption of Gemini Keys
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # Gemini (Optional for backend directly, but can be in .env)
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-1.5-flash"

    class Config:
        env_file = ".env"


settings = Settings()
