# User Guide

## Getting Started

### Creating Your Account

1. Open the application in your browser (http://localhost:8000)
2. Click "Sign Up"
3. Fill in your details:
   - **Username**: Your display name
   - **Email**: Used for login
   - **Password**: Choose a strong password
   - **Confirm Password**: Re-enter your password
   - **Auto-detect**: Check this to enable automatic transaction detection
4. Click "Sign up"

### Logging In

1. Enter your email and password
2. Click "Sign in"
3. You'll be taken to your dashboard

## Dashboard Overview

The dashboard shows:
- **Current Balance**: Your total balance across all transactions
- **Quick Stats**: Number of envelopes, goals, and transactions
- **Recent Transactions**: Your latest 10 transactions
- **Balance Forecast**: 30-day projection of your balance

## Managing Transactions

### Adding Transactions Manually

1. Click "Add Transaction" button
2. Fill in the form:
   - **Merchant**: Where you spent money (e.g., "Starbucks")
   - **Amount**: Enter negative for expenses, positive for income
   - **Date**: Transaction date
   - **Category**: Select from dropdown
   - **Envelope**: (Optional) Assign to a budget envelope
   - **Notes**: (Optional) Additional details
3. Click "Add"

### Importing Transactions

1. Go to "Transactions" page
2. Click "Import CSV/OFX"
3. Select your bank export file
4. Click "Import"
5. Review detected transactions
6. Accept or reject each transaction

**Supported Formats:**
- CSV files with columns: date, amount, merchant/description
- OFX/QFX files from most banks

### Detected Transactions

After importing, transactions appear in the "Detected" view with:
- **Confidence Badge**: High (green), Medium (yellow), or Low (red)
- **Normalized Merchant**: Cleaned up merchant name
- **Auto-assigned Category**: Based on merchant keywords

**Actions:**
- **Accept**: Adds transaction to your records
- **Reject**: Discards the transaction

## Budget Envelopes

Envelopes help you allocate money to specific spending categories.

### Creating an Envelope

1. Go to "Envelopes" page
2. Click "Create Envelope"
3. Enter:
   - **Name**: e.g., "Groceries", "Entertainment"
   - **Allocated Amount**: Your budget for this category
   - **Pooled**: Check if this is a shared/family envelope
4. Click "Create"

### Transferring Funds

Move money between envelopes:
1. Select "From Envelope"
2. Select "To Envelope"
3. Enter amount
4. Click "Transfer"

### Monitoring Spending

Each envelope shows:
- Allocated amount
- Amount spent
- Remaining balance
- Progress bar (visual indicator)

## Savings Goals

Track progress toward financial goals.

### Creating a Goal

1. Go to "Goals" page
2. Click "Create Goal"
3. Enter:
   - **Name**: e.g., "Emergency Fund", "Vacation"
   - **Target Amount**: Your goal amount
   - **Current Amount**: How much you've saved so far
   - **Deadline**: (Optional) Target date
4. Click "Create"

### Tracking Progress

Each goal displays:
- Percentage complete
- Current vs target amount
- Remaining amount needed
- Visual progress bar

## Forecasting

The forecast page helps you plan ahead.

### Understanding Your Forecast

- **Current Balance**: Your balance today
- **90-Day Projection**: Estimated balance in 90 days
- **Confidence Level**: How reliable the forecast is
  - **High**: 50+ transactions, recent data, recurring patterns
  - **Medium**: 20-50 transactions, some patterns
  - **Low**: Less than 20 transactions

### Spending Analysis

View your spending patterns:
- **Top Categories**: Where you spend the most
- **Top Merchants**: Your most frequent vendors
- **Monthly Trend**: Spending over time

## Online Sales

Track your e-commerce purchases separately.

The "Online Sales" page automatically shows transactions from:
- Amazon
- eBay
- PayPal
- Other online merchants

## Offers & Discounts

Manage promotional offers and discounts.

### Adding an Offer

1. Go to "Offers" page
2. Click "Add Offer"
3. Enter:
   - **Merchant**: Where the offer applies
   - **Discount**: Percentage off
   - **Description**: Offer details
   - **Expiry**: When the offer ends
4. Click "Add"

Active offers are displayed as cards with discount percentage.

## Recurring Transactions

Automatically detect recurring payments.

### How It Works

The system analyzes your transactions and identifies patterns:
- **Monthly**: Payments every 28-31 days
- **Weekly**: Payments every 6-8 days

### Viewing Recurring Items

Go to "Recurring" page to see:
- Merchant name
- Pattern type (Monthly/Weekly)
- Average amount
- Number of occurrences
- Last payment date
- Next expected date

## Reconciliation

Match your records against bank statements.

### Reconciling Your Account

1. Go to "Reconcile" page
2. Click "Choose File"
3. Select your bank statement (CSV format)
4. Click "Start Reconciliation"

### Understanding Results

The results page shows:
- **Matched**: Transactions found in both records (with confidence level)
- **Unmatched (Statement)**: Transactions in bank statement but not in your records
- **Unmatched (Your Records)**: Transactions you recorded but not in statement
- **Match Rate**: Percentage of successful matches

## Settings

Manage your account settings.

### Updating Profile

1. Go to "Settings" page
2. Update your username
3. Toggle auto-detect transactions
4. Click "Save Changes"

### Exporting Data

**CSV Export:**
- Click "Export to CSV"
- Downloads all your transactions

**Encrypted Backup:**
- Click "Create Encrypted Backup"
- Enter a passphrase
- Downloads encrypted backup file
- **Important**: Remember your passphrase!

## Tips & Best Practices

### For Accurate Forecasting
- Add transactions regularly
- Include both income and expenses
- Use consistent categories
- Import bank statements monthly

### For Better Auto-Detection
- Enable auto-detect in settings
- Review and accept detected transactions promptly
- The system learns from your patterns

### For Effective Budgeting
- Create envelopes for major spending categories
- Review envelope spending weekly
- Adjust allocations as needed
- Use pooled envelopes for shared expenses

### For Goal Achievement
- Set realistic targets
- Update current amounts regularly
- Set deadlines to stay motivated
- Break large goals into smaller milestones

## Troubleshooting

### Transactions Not Appearing
- Check that you're logged in
- Verify the transaction was saved (check for success message)
- Refresh the page

### Import Failing
- Ensure CSV has required columns (date, amount, merchant)
- Check date format (YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY)
- Verify file is not corrupted

### Forecast Shows Low Confidence
- Add more transactions (need 20+ for medium confidence)
- Ensure transactions are recent (within last 30 days)
- Add recurring transactions to improve accuracy

### Can't See Recurring Patterns
- Need at least 2 occurrences of same merchant
- Transactions must be roughly same interval apart
- Check that merchant names match exactly

## Data Privacy & Security

- Passwords are hashed using bcrypt
- Each user's data is isolated
- Transaction logs stored in separate files per user
- Encrypted backups protect your data
- No data is shared with third parties
- All data stored locally on your machine

## Keyboard Shortcuts

- **Esc**: Close modal dialogs
- **Tab**: Navigate form fields
- **Enter**: Submit forms

## Support

For technical issues:
1. Check the SETUP.md file
2. Review PROJECT_TASKS.md for known issues
3. Ensure all dependencies are installed
4. Try restarting the application
