@echo off
echo ================================================
echo   Starting LETS GO Bus Service Backend
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the Flask server
echo Starting Flask server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py
