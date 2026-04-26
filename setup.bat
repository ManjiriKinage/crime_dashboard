@echo off
REM Crime Record Management System - Windows Installation Script
REM This script sets up the entire project on Windows

echo.
echo ========================================
echo   CRIME MANAGEMENT SYSTEM - SETUP SCRIPT
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version
echo OK

echo.
echo [2/4] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo Virtual environment created
)

echo.
echo [3/4] Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully

echo.
echo [4/4] Setup complete!
echo.
echo ========================================
echo   NEXT STEPS
echo ========================================
echo.
echo 1. Update database credentials:
echo    - Edit db_config.py
echo    - Set your MySQL password
echo.
echo 2. Setup MySQL database:
echo    - Ensure MySQL is running
echo    - Run: mysql -u root -p ^< setup_database.sql
echo.
echo 3. Run the application:
echo    - Run: run_app.bat
echo.
echo ========================================
echo.
pause
