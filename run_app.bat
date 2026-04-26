@echo off
REM Crime Record Management System - Windows Run Script
REM This script runs the Streamlit application

echo.
echo ========================================
echo   CRIME MANAGEMENT SYSTEM - STARTING
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if MySQL is running (optional)
echo Checking for MySQL server...
netstat -an | findstr :3306 >nul
if errorlevel 1 (
    echo WARNING: MySQL server might not be running on port 3306
    echo Ensure MySQL is started before proceeding
    echo.
)

REM Run Streamlit
echo Starting Streamlit application...
echo.
echo ========================================
echo Local URL: http://localhost:8501
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py

pause
