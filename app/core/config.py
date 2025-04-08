import os
from typing import Any, Dict, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "OpenAI Analysis API"
    PROJECT_DESCRIPTION: str = "REST API that processes messages through OpenAI using LangChain"
    VERSION: str = "1.0.0"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL_NAME: str = "gpt-4o-mini"
    OPENAI_TEMPERATURE: float = 0.7

    # Database Settings
    # DB_USERNAME: str = os.getenv("DB_USERNAME", "root")
    # DB_PASSWORD: str = os.getenv("DB_PASSWORD", "admin1234")
    # DB_NAME: str = os.getenv("DB_NAME", "telegram_db")
    # DB_HOST: str = os.getenv("DB_HOST", "localhost")
    # DB_PORT: str = os.getenv("DB_PORT", "5432")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://root:admin1234@localhost:5432/telegram_db")

    @field_validator("OPENAI_API_KEY")
    def validate_openai_api_key(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        return v
    
    class Config:
        case_sensitive = True


settings = Settings() 