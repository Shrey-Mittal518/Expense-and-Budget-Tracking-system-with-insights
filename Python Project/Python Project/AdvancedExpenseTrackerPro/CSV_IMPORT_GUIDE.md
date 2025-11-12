# CSV Import Guide - Transaction Type Detection

## Overview

The system now automatically detects whether transactions are **income** or **expenses** from your CSV files using intelligent keyword matching.

## Supported CSV Formats

### Format 1: With Type Column

```csv
date,amount,merchant,description,type
2024-01-15,500,Grocery Store,Weekly shopping,debit
2024-01-20,5000,Company Name,Salary payment,credit
```

### Format 2: With Transaction Type Column

```csv
date,amount,merchant,transaction type
2024-01-15,500,Grocery Store,spent
2024-01-20,5000,Company Name,received
```

### Format 3: With CR/DR Column

```csv
date,amount,merchant,cr/dr
2024-01-15,500,Grocery Store,DR
2024-01-20,5000,Company Name,CR
```

## Recognized Keywords

### Income Keywords (Positive/Credit)
The system recognizes these words as **income**:
- credit
- deposit
- salary
- income
- received / receive
- refund
- cashback
- reward
- bonus
- payment received
- transfer in
- credited
- earn / earned
- revenue
- sale / sold
- interest
- dividend

### Expense Keywords (Negative/Debit)
The system recognizes these words as **expenses**:
- debit
- withdrawal
- payment
- purchase
- spent / spend
- paid
- bill
- charge
- fee
- transfer out
- debited
- bought / buy
- expense
- cost
- shopping
- subscription

## How It Works

### Step 1: Column Detection
The system looks for columns with these names:
- `type`
- `transaction type`
- `trans type`
- `txn type`
- `mode`
- `cr/dr`
- `description`
- `memo`
- `narration`
- `details`
- `remarks`

### Step 2: Keyword Matching
Once a column is found, it searches for income or expense keywords in the value.

### Step 3: Amount Adjustment
- If keyword indicates **expense** → amount becomes negative
- If keyword indicates **income** → amount becomes positive

## Examples

### Example 1: Bank Statement Format

**CSV File:**
```csv
Date,Description,Amount,Type
01/15/2024,Grocery Store,500,Debit
01/20/2024,Salary Credit,5000,Credit
01/22/2024,ATM Withdrawal,1000,Debit
```

**Result:**
- Grocery Store: -₹500 (Expense, red)
- Salary Credit: +₹5000 (Income, green)
- ATM Withdrawal: -₹1000 (Expense, red)

### Example 2: Credit Card Statement

**CSV File:**
```csv
Transaction Date,Merchant,Amount,Transaction Type
2024-01-15,Amazon,2500,Purchase
2024-01-18,Refund - Amazon,500,Credit
2024-01-20,Restaurant,800,Spent
```

**Result:**
- Amazon: -₹2500 (Expense, red)
- Refund - Amazon: +₹500 (Income, green)
- Restaurant: -₹800 (Expense, red)

### Example 3: Paytm/UPI Statement

**CSV File:**
```csv
Date,Description,Amount,Mode
15-01-2024,Payment to merchant,300,Sent
20-01-2024,Received from friend,500,Received
22-01-2024,Bill payment,1000,Paid
```

**Result:**
- Payment to merchant: -₹300 (Expense, red)
- Received from friend: +₹500 (Income, green)
- Bill payment: -₹1000 (Expense, red)

## Testing Your CSV

### Sample CSV Template

Create a file named `my_transactions.csv`:

```csv
date,amount,merchant,type
2024-01-15,500,Grocery Store,debit
2024-01-16,200,Coffee Shop,spent
2024-01-20,5000,Salary,credit
2024-01-22,1000,Rent,payment
2024-01-25,300,Refund,received
```

### Import Steps

1. Go to **Transactions** page
2. Click **Import CSV/OFX**
3. Select your CSV file
4. Click **Import**
5. Review detected transactions
6. Check that:
   - Expenses show in **red** with **-** sign
   - Income shows in **green** with **+** sign
7. Click **Accept** for each transaction

## Troubleshooting

### Issue: All transactions showing as expenses

**Solution:** Check your CSV has a type column with keywords like:
- For income: `credit`, `received`, `salary`, `income`
- For expenses: `debit`, `spent`, `payment`, `purchase`

### Issue: Amounts are wrong sign

**Solution:** The system auto-adjusts based on keywords. Make sure:
- Income keywords → positive amount
- Expense keywords → negative amount

### Issue: Type column not detected

**Solution:** Rename your column to one of these:
- `type`
- `transaction type`
- `cr/dr`

Or add keywords to the `description` column.

## Best Practices

1. **Use Standard Column Names**
   - `date` for transaction date
   - `amount` for transaction amount
   - `merchant` or `description` for merchant name
   - `type` for transaction type

2. **Be Consistent with Keywords**
   - Use same keyword for all expenses (e.g., always use "debit")
   - Use same keyword for all income (e.g., always use "credit")

3. **Include Description**
   - Even if you have a type column, include description
   - Helps with merchant detection and categorization

4. **Test with Small File First**
   - Import 5-10 transactions first
   - Verify they're detected correctly
   - Then import full statement

## Advanced: Multiple Bank Formats

### HDFC Bank Format
```csv
Date,Narration,Chq./Ref.No.,Value Dt,Withdrawal Amt.,Deposit Amt.,Closing Balance
01/15/2024,UPI-GROCERY STORE,123456,01/15/2024,500.00,,45000.00
01/20/2024,SALARY CREDIT,SAL001,01/20/2024,,50000.00,95000.00
```

**Detection:** System looks at Withdrawal/Deposit columns
- Withdrawal → Expense
- Deposit → Income

### ICICI Bank Format
```csv
Date,Description,Debit,Credit,Balance
15-01-2024,GROCERY STORE,500,,44500
20-01-2024,SALARY,,50000,94500
```

**Detection:** System checks Debit/Credit columns
- Debit → Expense
- Credit → Income

### SBI Bank Format
```csv
Txn Date,Description,Ref No./Cheque No.,Debit,Credit,Balance
15/01/2024,GROCERY STORE,UPI123,500.00,,44500.00
20/01/2024,SALARY CREDIT,SAL001,,50000.00,94500.00
```

**Detection:** Similar to ICICI format

## Quick Reference

| Your CSV Says | System Interprets As | Display |
|---------------|---------------------|---------|
| debit, spent, payment | Expense | -₹500 (red) |
| credit, received, salary | Income | +₹5000 (green) |
| purchase, bought | Expense | -₹300 (red) |
| refund, cashback | Income | +₹200 (green) |

## Need Help?

If your CSV format isn't working:
1. Check column names match supported formats
2. Verify keywords are in the list above
3. Try adding a `type` column manually
4. Use the sample CSV as a template

---

**Pro Tip:** Most banks allow you to download statements in CSV format. Look for "Export" or "Download Statement" options in your online banking portal.
