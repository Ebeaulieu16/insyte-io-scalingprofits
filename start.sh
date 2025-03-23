#!/bin/bash

# Insyte.io Startup Script
# This script starts both the backend and frontend servers

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Insyte.io...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.9 or higher.${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install Node.js 18 or higher.${NC}"
    exit 1
fi

# Check if the backend .env file exists
if [ ! -f "./backend/.env" ]; then
    echo -e "${YELLOW}Backend .env file not found. Creating from example...${NC}"
    cp ./backend/.env.example ./backend/.env
    echo -e "${YELLOW}Please edit ./backend/.env with your API keys.${NC}"
fi

# Start the backend
echo -e "${GREEN}Starting backend server...${NC}"
cd backend

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}Activated virtual environment.${NC}"
else
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    
    # Install dependencies
    echo -e "${GREEN}Installing backend dependencies...${NC}"
    pip install -r requirements.txt
fi

# Start the backend server in the background
python run.py &
BACKEND_PID=$!
echo -e "${GREEN}Backend server started with PID ${BACKEND_PID}.${NC}"

# Start the frontend
echo -e "${GREEN}Starting frontend server...${NC}"
cd ../frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Frontend dependencies not found. Installing...${NC}"
    npm install
fi

# Start the frontend server
echo -e "${GREEN}Starting frontend development server...${NC}"
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}Frontend server started with PID ${FRONTEND_PID}.${NC}"

# Display access information
echo ""
echo -e "${GREEN}Insyte.io is now running!${NC}"
echo -e "Backend API: ${YELLOW}http://localhost:8001${NC}"
echo -e "Frontend UI: ${YELLOW}http://localhost:5173${NC}"
echo -e "API Documentation: ${YELLOW}http://localhost:8001/docs${NC}"
echo -e "API Status: ${YELLOW}http://localhost:8001/status/health${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both servers.${NC}"

# Function to clean up when the script is stopped
cleanup() {
    echo -e "${YELLOW}Stopping servers...${NC}"
    kill $BACKEND_PID
    kill $FRONTEND_PID
    echo -e "${GREEN}Servers stopped. Goodbye!${NC}"
    exit 0
}

# Trap to catch interrupt signal
trap cleanup SIGINT

# Keep the script running
wait 