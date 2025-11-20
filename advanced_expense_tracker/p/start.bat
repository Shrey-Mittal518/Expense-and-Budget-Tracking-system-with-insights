@echo off
echo Starting AdvancedExpenseTrackerPro...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo.
)

REM Start the application
echo Starting application on http://localhost:8000
echo Press Ctrl+C to stop
echo.
python run.py
