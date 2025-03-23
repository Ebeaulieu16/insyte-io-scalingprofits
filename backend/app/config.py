import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IS_PRODUCTION = ENVIRONMENT == "production"

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./insyte.db")
# Handle special case for Postgres with SSL (Heroku/Render style URL)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# API Keys
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
CALENDLY_API_KEY = os.getenv("CALENDLY_API_KEY")
CALENDLY_WEBHOOK_SECRET = os.getenv("CALENDLY_WEBHOOK_SECRET")
CALCOM_API_KEY = os.getenv("CALCOM_API_KEY")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "default-insecure-key")
# Authentication settings
AUTH_USERNAME = os.getenv("AUTH_USERNAME", "admin")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "changeThisPassword!")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# API Settings
API_V1_PREFIX = "/api/v1"

# URL Settings
BASE_URL = os.getenv("BASE_URL", "http://localhost:8001")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# CORS Settings - in production, use the FRONTEND_URL
if IS_PRODUCTION:
    CORS_ORIGINS = [FRONTEND_URL]
else:
    CORS_ORIGINS = [
        "http://localhost:5173",  # Frontend dev server
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://localhost:5177",
        "http://localhost:3000",  # Alternative frontend port
        "https://yourdomain.com",  # Production domain
    ]

# Application Settings
APP_NAME = "Insyte.io API"
APP_DESCRIPTION = "API for YouTube video performance and sales funnel tracking"
APP_VERSION = "0.1.0"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

# Scheduled task settings
YOUTUBE_REFRESH_INTERVAL = int(os.getenv("YOUTUBE_REFRESH_INTERVAL", "6"))  # hours 