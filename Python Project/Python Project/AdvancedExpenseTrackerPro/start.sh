#!/bin/bash

echo "Starting AdvancedExpenseTrackerPro..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ""
fi

# Start the application
echo "Starting application on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""
python run.py
