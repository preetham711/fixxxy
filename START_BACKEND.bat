@echo off
echo ========================================
echo FIXXY Backend Server
echo ========================================
echo.

cd /d "%~dp0backend"

echo Checking virtual environment...
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo.
echo Starting FastAPI backend on http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
