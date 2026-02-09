"""Configuration management"""

import os
from functools import lru_cache

# Load .env file only if it exists (for local development)
# Railway provides environment variables directly, so .env is optional
try:
    from dotenv import load_dotenv
    if os.path.exists(".env"):
        load_dotenv()
        print("✅ Loaded .env file for local development")
except ImportError:
    print("⚠️  python-dotenv not installed, using environment variables only")
except Exception as e:
    print(f"⚠️  Could not load .env: {e}")


class Settings:
    """Application settings"""

    def __init__(self):
        # API Keys - Read directly from environment
        self.google_api_key = os.environ.get("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")

        # Model Configuration
        self.default_model = os.environ.get("DEFAULT_MODEL", "gemini-1.5-flash-latest")
        self.complex_model = os.environ.get("COMPLEX_MODEL", "gemini-1.5-pro-latest")

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
