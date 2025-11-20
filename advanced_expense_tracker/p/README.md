# AdvancedExpenseTrackerPro

A modern, full-featured expense tracking web application built with Python, Flask, and vanilla JavaScript.

## Features

- **User Authentication**: Secure signup/login with password hashing
- **Transaction Management**: Add, edit, delete, and categorize expenses
- **Auto-Detection**: Rule-based transaction detection from CSV/OFX imports
- **Envelopes**: Budget allocation with pooled/shared envelope support
- **Goals Tracking**: Set and monitor savings targets
- **Forecasting**: Rule-based balance projection engine
- **Online Sales**: Dedicated ecommerce transaction tracking
- **Offers System**: Apply discounts and promotional offers
- **Recurring Detection**: Automatic identification of recurring payments
- **Reconciliation**: Match transactions against bank statements
- **Per-User Storage**: SQLite database + individual transaction log files
- **Data Export**: CSV export and encrypted backups

## Tech Stack

- **Backend**: Python 3.10+, Flask
- **Frontend**: HTML5, CSS3 (Tailwind CSS), Vanilla JavaScript (ES6)
- **Database**: SQLite
- **Authentication**: Flask-Login with bcrypt password hashing
- **Testing**: pytest

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python run.py
   ```

3. **Access the app**:
   Open your browser to `http://localhost:8000`

4. **Sign up**: Create a new account to get started

## Project Structure

```
AdvancedExpenseTrackerPro/
├── app.py                  # Main Flask application
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── models/                 # Data models
│   ├── user.py
│   ├── transaction.py
│   └── envelope.py
├── services/              # Business logic
│   ├── data_store.py
│   ├── auto_detect.py
│   ├── forecaster.py
│   ├── offers.py
│   └── reconciliation.py
├── templates/             # Jinja2 templates
├── static/               # CSS, JS, images
├── data/                 # SQLite DB and user files
├── tests/                # Unit tests
└── docs/                 # Documentation
```

## Testing

Run the test suite:
```bash
pytest
```

## Security Notes

- Passwords are hashed using bcrypt
- Per-user data isolation
- Path traversal protection for file operations
- Session-based authentication

## Documentation

See the `docs/` folder for detailed guides:
- `SETUP.md` - Installation and configuration
- `PROJECT_TASKS.md` - Development roadmap and tasks
