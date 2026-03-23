@echo off
TITLE Cow Breed Classifier - Complete Application
echo =================================================
echo Starting Cow Breed Classifier Application
echo =================================================

echo This script will start both the backend and frontend servers.
echo Please wait for both servers to initialize completely.
echo.
echo Backend server:   http://127.0.0.1:8000
echo Frontend server:  http://localhost:3000
echo.

REM Start backend server in a new minimized window
start /min cmd /c "cd backend && title Backend Server && python start_server.py"

REM Wait a few seconds for backend to start
echo Waiting for backend server to start...
timeout /t 5 /nobreak >nul

REM Start frontend server in a new window
start cmd /c "cd frontend && title Frontend Server && npm run dev"

echo.
echo Both servers are starting up...
echo Once ready, open your browser to http://localhost:3000
echo.
echo NOTE: Do not close this window until you're done using the application
echo Press CTRL+C and confirm to stop both servers when finished

pause