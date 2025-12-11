"""
Configuration settings for the textbook generation backend
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Textbook Generation Backend"
    app_version: str = "0.1.0"
    admin_email: str = "admin@example.com"
    
    # Database settings
    database_url: str = "postgresql+asyncpg://username:password@localhost:5432/textbook_db"
    
    # Qdrant settings
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    
    # LLM Provider settings
    llm_provider_api_key: str = ""
    embedding_model_name: str = "text-embedding-3-small"
    
    # Application settings
    app_env: str = "development"  # development, staging, production
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"


settings = Settings()