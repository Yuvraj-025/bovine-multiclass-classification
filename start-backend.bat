@echo off
TITLE Cow Breed Classifier - Backend Server
echo ========================================
echo Starting Cow Breed Classifier Backend...
echo ========================================

cd backend
echo Current directory: %CD%

echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Installing/Updating Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Failed to install/update dependencies
    echo Continuing with existing installation...
)

echo Starting FastAPI server...
echo Server will be available at http://127.0.0.1:8000
echo.

python start_server.py

pause