# Setup Guide

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (optional, for version control)

## Installation Steps

### 1. Clone or Download the Project

```bash
cd AdvancedExpenseTrackerPro
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` and set your configuration:
```
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_PATH=data/expense_tracker.db
USER_DATA_PATH=data/users
PORT=8000
```

**Important:** Change the `SECRET_KEY` to a random string for production use.

### 5. Initialize the Application

The database will be automatically created on first run. Simply start the application:

```bash
python run.py
```

### 6. Access the Application

Open your web browser and navigate to:
```
http://localhost:8000
```

## First Time Setup

1. Click "Sign Up" to create your account
2. Fill in:
   - Username
   - Email address
   - Password (and confirm)
   - Check "Enable auto-detect transactions" if desired
3. Click "Sign up"
4. You'll be automatically logged in

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, change the `PORT` in your `.env` file:
```
PORT=5000
```

### Database Errors

If you encounter database errors, delete the database file and restart:
```bash
del data\expense_tracker.db
python run.py
```

### Module Not Found Errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Permission Errors

On Windows, you may need to run as administrator. On macOS/Linux:
```bash
chmod +x run.py
```

## Running Tests

To run the test suite:
```bash
pytest
```

For verbose output:
```bash
pytest -v
```

For coverage report:
```bash
pytest --cov=services --cov=models
```

## Development Mode

The application runs in debug mode by default. For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:create_app()
   ```

## Data Backup

Your data is stored in:
- SQLite database: `data/expense_tracker.db`
- User transaction logs: `data/users/<user_id>.txt`

Regularly backup these files to prevent data loss.

## Updating

To update dependencies:
```bash
pip install -r requirements.txt --upgrade
```

## Uninstallation

1. Deactivate virtual environment: `deactivate`
2. Delete the project folder
3. Your data will be lost unless backed up

## Support

For issues or questions, refer to the main README.md or check the PROJECT_TASKS.md for known issues.
