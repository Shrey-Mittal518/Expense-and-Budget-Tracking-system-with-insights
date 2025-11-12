# Quick Start Guide

## 🚀 Get Running in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python run.py
```

### Step 3: Open in Browser
```
http://localhost:8000
```

## 📝 First Time Setup

1. **Sign Up**
   - Click "Sign Up" button
   - Enter username, email, password
   - Check "Enable auto-detect transactions"
   - Click "Sign up"

2. **Add Your First Transaction**
   - Click "Add Transaction" on dashboard
   - Fill in merchant, amount, date, category
   - Click "Add"

3. **Import Bank Statement** (Optional)
   - Go to "Transactions" page
   - Click "Import CSV/OFX"
   - Select your bank export file
   - Review and accept detected transactions

## 🎯 Key Features

### Transactions
- **Manual Entry**: Add expenses and income manually
- **Import**: Upload CSV or OFX files from your bank
- **Auto-Detect**: Automatic merchant and category detection

### Budgeting
- **Envelopes**: Allocate money to spending categories
- **Goals**: Track savings targets with progress bars
- **Forecasting**: See projected balance for next 90 days

### Analysis
- **Recurring**: Automatically detect recurring payments
- **Online Sales**: Track e-commerce purchases separately
- **Reconciliation**: Match transactions against bank statements

### Data Management
- **Export**: Download transactions as CSV
- **Backup**: Create encrypted backups with passphrase
- **Security**: All passwords hashed, data isolated per user

## 📁 Sample Data

Try importing the sample CSV:
```
sample_data/sample_transactions.csv
```

This includes 20 sample transactions to test the import and auto-detection features.

## 🧪 Run Tests

```bash
pytest
```

For verbose output:
```bash
pytest -v
```

## 📚 Documentation

- **SETUP.md** - Detailed installation instructions
- **USER_GUIDE.md** - Complete user documentation
- **PROJECT_TASKS.md** - Development roadmap
- **SUMMARY.md** - Technical overview

## 🔧 Configuration

Edit `.env` file to customize:
```
SECRET_KEY=your-secret-key
DATABASE_PATH=data/expense_tracker.db
USER_DATA_PATH=data/users
PORT=8000
```

## 🐛 Troubleshooting

**Port already in use?**
- Change `PORT=5000` in `.env` file

**Module not found?**
- Run: `pip install -r requirements.txt --upgrade`

**Database errors?**
- Delete `data/expense_tracker.db` and restart

## 💡 Tips

1. **Enable auto-detect** during signup for automatic transaction categorization
2. **Import regularly** to keep your data up-to-date
3. **Create envelopes** for major spending categories
4. **Set goals** to stay motivated
5. **Review forecast** weekly to stay on track

## 🎨 UI Navigation

- **Home** - Dashboard with balance and recent transactions
- **Transactions** - View and manage all transactions
- **Envelopes** - Budget allocation and tracking
- **Goals** - Savings targets
- **Forecast** - Balance projections and analytics
- **Online Sales** - E-commerce purchases
- **Offers** - Discounts and promotions
- **Recurring** - Recurring payment patterns
- **Reconcile** - Match against bank statements
- **Settings** - Account settings and data export

## 🔐 Security Notes

- Passwords are hashed with bcrypt (never stored in plain text)
- Each user's data is completely isolated
- Transaction logs stored in separate files per user
- Encrypted backup option available
- No data shared with third parties

## 📊 Data Storage

Your data is stored in:
- **Database**: `data/expense_tracker.db` (SQLite)
- **Transaction Logs**: `data/users/<user_id>.txt`
- **Offers**: `data/offers.json`

**Backup regularly!**

## 🚦 System Requirements

- Python 3.10 or higher
- 50 MB disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for Tailwind CSS CDN and Google Fonts)

## 📞 Need Help?

Check the documentation:
1. Read **USER_GUIDE.md** for detailed instructions
2. Review **SETUP.md** for installation issues
3. Check **PROJECT_TASKS.md** for known issues

## ✅ Verification Checklist

After installation, verify:
- [ ] Server starts without errors
- [ ] Can access http://localhost:8000
- [ ] Can create an account
- [ ] Can add a transaction
- [ ] Transaction appears in list
- [ ] Can import sample CSV
- [ ] Tests pass with `pytest`

## 🎉 You're Ready!

Start tracking your expenses and take control of your finances!

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**License:** Original Implementation
