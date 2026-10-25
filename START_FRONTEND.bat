@echo off
echo ========================================
echo FIXXY Frontend Server
echo ========================================
echo.

cd /d "%~dp0frontend"

echo Starting React development server...
echo Frontend will open at: http://localhost:5173
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

npm run dev

pause
