@echo off
REM Fake News Detection Flask App Launcher

cd /d "%~dp0"

echo ============================================
echo   Fake News Detection Web App
echo ============================================
echo.

echo Starting Flask application...
echo Open your browser: http://127.0.0.1:5000
echo.

.\.venv\Scripts\python.exe app.py

pause
