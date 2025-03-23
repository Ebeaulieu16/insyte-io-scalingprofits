import sys
import os
import importlib.util
from pathlib import Path
import logging

# Add the parent directory to sys.path to allow absolute imports
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import config settings
from app.config import (
    APP_NAME, 
    APP_DESCRIPTION, 
    APP_VERSION, 
    CORS_ORIGINS,
    IS_PRODUCTION
)

# Import directly from the model files
from app.database import engine
from app.models import Base

# Import the routes
from app.routes import dashboard, links, redirect, webhooks, status, auth

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create tables - with error handling for production databases
try:
    logger.info("Attempting to create database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")
    if IS_PRODUCTION:
        logger.warning("In production environment, database migrations should be handled carefully")
        logger.warning("Consider using Alembic for database migrations in production")
    else:
        # In development, we can re-raise the error
        raise

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(dashboard.router)
app.include_router(links.router)
app.include_router(redirect.router)
app.include_router(webhooks.router)
app.include_router(status.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {APP_NAME}",
        "docs": "/docs",
        "version": APP_VERSION,
        "status": "/status/health"
    }

# Run the application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True) 