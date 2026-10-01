"""
FIELD PLUS — Configuration Settings
Handles environment variable loading, database parameters, and Flask configurations.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Load variables from .env file if it exists
load_dotenv(BASE_DIR / ".env")


class Config:
    """Base configuration class with common defaults."""

    SECRET_KEY = os.getenv("SECRET_KEY", "field_plus_default_dev_key_change_me_987654")
    
    # Database Settings
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "field_plus_db")
    
    # Session Configuration
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours in seconds

    # Application Branding
    APP_NAME = "FIELD PLUS"
    APP_TAGLINE = "Field Work & Task Management System"


class DevelopmentConfig(Config):
    """Configuration for local development."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Configuration for automated test execution."""
    DEBUG = False
    TESTING = True
    DB_NAME = os.getenv("TEST_DB_NAME", "field_plus_test_db")


class ProductionConfig(Config):
    """Configuration for production deployment."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Requires HTTPS


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
