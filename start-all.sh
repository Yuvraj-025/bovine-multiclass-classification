#!/bin/bash

# Cow Breed Classifier - Start Script for Linux/Mac

echo "================================================="
echo "Starting Cow Breed Classifier Application"
echo "================================================="

echo "This script will start both the backend and frontend servers."
echo "Please wait for both servers to initialize completely."
echo ""
echo "Backend server:   http://127.0.0.1:8000"
echo "Frontend server:  http://localhost:3000"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
if ! command_exists python3; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi

if ! command_exists node; then
    echo "ERROR: Node.js is not installed or not in PATH"
    echo "Please install Node.js 14+ and try again"
    exit 1
fi

# Start backend server
echo "Starting backend server..."
cd backend
pip install -r requirements.txt >/dev/null 2>&1 &
python start_server.py &
cd ..

# Wait a few seconds for backend to start
echo "Waiting for backend server to start..."
sleep 5

# Start frontend server
echo "Starting frontend server..."
cd frontend
npm install >/dev/null 2>&1
npm run dev &
cd ..

echo ""
echo "Both servers are starting up..."
echo "Once ready, open your browser to http://localhost:3000"
echo ""
echo "NOTE: Do not close this terminal until you're done using the application"
echo "Press CTRL+C to stop both servers when finished"

# Wait for background processes
wait