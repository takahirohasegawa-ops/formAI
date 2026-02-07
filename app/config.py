"""Configuration management"""

import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # API Keys
    google_api_key: str

    # Model Configuration
    default_model: str = "gemini-1.5-flash"
    complex_model: str = "gemini-1.5-pro"

    # Sender Information
    company_name: str = "RECHANCE株式会社"
    contact_person: str = "桑原麻由"
    email: str = "info@rechance.jp"
    phone: str = "090-1234-7891"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = int(os.environ.get("PORT", "8000"))

    # Browser Configuration
    headless: bool = True
    timeout: int = 60000  # 60 seconds

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Allow environment variables to override .env file
        env_prefix = ""


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
