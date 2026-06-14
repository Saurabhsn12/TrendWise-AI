"""
TrendWise AI — Configuration Module
Centralizes all application settings and environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    """Base configuration class."""

    # Flask Core
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Database
    DATABASE_PATH = os.path.join(BASE_DIR, os.environ.get('DATABASE_PATH', 'trendwise.db'))

    # AI Configuration (used in Phase 3+)
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'local')  # 'gemini', 'huggingface', 'local'

    # Alpha Vantage (optional)
    ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY', '')

    # Session Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True


# Configuration map for easy switching
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
