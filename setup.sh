#!/bin/bash
# Crime Record Management System - Unix/Linux/Mac Installation Script

echo ""
echo "========================================"
echo "  CRIME MANAGEMENT SYSTEM - SETUP"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ using:"
    echo "  - Mac: brew install python3"
    echo "  - Linux: sudo apt-get install python3"
    exit 1
fi

echo "[1/4] Checking Python installation..."
python3 --version
echo "OK"

echo ""
echo "[2/4] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "Virtual environment created"
fi

echo ""
echo "[3/4] Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "Dependencies installed successfully"

echo ""
echo "[4/4] Setup complete!"
echo ""
echo "========================================"
echo "   NEXT STEPS"
echo "========================================"
echo ""
echo "1. Update database credentials:"
echo "   - Edit db_config.py"
echo "   - Set your MySQL password"
echo ""
echo "2. Setup MySQL database:"
echo "   - Ensure MySQL is running"
echo "   - Run: mysql -u root -p < setup_database.sql"
echo ""
echo "3. Run the application:"
echo "   - Run: ./run_app.sh"
echo ""
echo "========================================"
echo ""
