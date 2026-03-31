@echo off
echo ================================================
echo   LETS GO Bus Service - Setup Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Python found!
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [2/5] Creating virtual environment...
    python -m venv venv
) else (
    echo [2/5] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
pip install -r requirements.txt
echo.

REM Prompt for database setup
echo [5/5] Database Setup
echo.
echo Before initializing the database, make sure:
echo   1. PostgreSQL is installed and running
echo   2. You have created a database named 'lets_go_bus'
echo   3. You have updated the .env file with your PostgreSQL password
echo.
set /p INIT_DB="Do you want to initialize the database now? (Y/N): "
if /i "%INIT_DB%"=="Y" (
    echo.
    echo Initializing database...
    python init_db.py
) else (
    echo.
    echo You can initialize the database later by running: python init_db.py
)

echo.
echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo To start the backend server, run:
echo   venv\Scripts\activate
echo   python app.py
echo.
echo Or simply run: start_server.bat
echo.
pause
