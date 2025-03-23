#!/bin/bash

# Render.com startup script for Insyte.io backend

# Exit on error
set -e

# Log startup
echo "Starting Insyte.io backend..."

# Print Python & pip versions
python --version
pip --version

# Install dependencies (in case they weren't installed in the build phase)
pip install -r requirements.txt

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL database to be ready..."
sleep 5  # Simple wait to ensure database is up

# Run the application using Uvicorn
echo "Starting web server..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT 