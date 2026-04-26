#!/bin/bash
# Crime Record Management System - Unix/Linux/Mac Run Script

echo ""
echo "========================================"
echo "  CRIME MANAGEMENT SYSTEM - STARTING"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if MySQL is running (optional)
echo "Checking for MySQL server..."
if ! nc -z localhost 3306 2>/dev/null; then
    echo "WARNING: MySQL server might not be running on port 3306"
    echo "Ensure MySQL is started before proceeding"
    echo ""
fi

# Run Streamlit
echo "Starting Streamlit application..."
echo ""
echo "========================================"
echo "Local URL: http://localhost:8501"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
