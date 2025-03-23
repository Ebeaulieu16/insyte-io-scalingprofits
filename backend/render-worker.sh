#!/bin/bash

# Render.com worker startup script for Insyte.io

# Exit on error
set -e

# Log startup
echo "Starting Insyte.io worker process..."

# Print Python & pip versions
python --version
pip --version

# Install dependencies (in case they weren't installed in the build phase)
pip install -r requirements.txt

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL database to be ready..."
sleep 10  # Simple wait to ensure database is up

# Run the worker process
echo "Starting worker process..."
exec python worker.py 