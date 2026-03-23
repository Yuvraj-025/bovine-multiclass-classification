@echo off
TITLE Cow Breed Classifier - Frontend Server
echo ========================================
echo Starting Cow Breed Classifier Frontend...
echo ========================================

cd frontend
echo Current directory: %CD%

echo Checking Node.js environment...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 14+ and try again
    pause
    exit /b 1
)

npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is not installed or not in PATH
    pause
    exit /b 1
)

echo Installing/Updating Node.js dependencies...
npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo Starting React development server...
echo Frontend will be available at http://localhost:3000
echo.

npm run dev

pause