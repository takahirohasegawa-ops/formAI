"""Configuration management"""

import os
from functools import lru_cache
from dotenv import load_dotenv

# Load .env file if it exists (for local development)
load_dotenv()


class Settings:
    """Application settings"""

    def __init__(self):
        # API Keys - Read directly from environment
        self.google_api_key = os.environ.get("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")

        # Model Configuration
        self.default_model = os.environ.get("DEFAULT_MODEL", "gemini-1.5-flash")
        self.complex_model = os.environ.get("COMPLEX_MODEL", "gemini-1.5-pro")

        # Sender Information
        self.company_name = os.environ.get("COMPANY_NAME", "RECHANCE株式会社")
        self.contact_person = os.environ.get("CONTACT_PERSON", "桑原麻由")
        self.email = os.environ.get("EMAIL", "info@rechance.jp")
        self.phone = os.environ.get("PHONE", "090-1234-7891")

        # API Configuration
        self.api_host = os.environ.get("API_HOST", "0.0.0.0")
        self.api_port = int(os.environ.get("PORT", os.environ.get("API_PORT", "8000")))

        # Browser Configuration
        self.headless = os.environ.get("HEADLESS", "true").lower() == "true"
        self.timeout = int(os.environ.get("TIMEOUT", "60000"))


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
