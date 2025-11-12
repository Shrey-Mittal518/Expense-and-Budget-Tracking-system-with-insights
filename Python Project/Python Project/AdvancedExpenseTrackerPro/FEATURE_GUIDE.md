# Feature Guide - Quick Reference

## 🌓 Dark/Light Theme Toggle

**Location**: Top right corner of navigation bar

**How to use**:
1. Click the 🌓 moon icon
2. Theme switches instantly
3. Preference saved automatically

**Benefits**:
- Dark theme: Better for night use, reduces eye strain
- Light theme: Better for bright environments, default look

---

## 💰 Income vs Expense Tracking

### How to Enter Transactions

**For Expenses** (money you spend):
```
Amount: -50
Example: -500 for groceries, -1000 for rent
```

**For Income** (money you receive):
```
Amount: 1000
Example: 5000 for salary, 200 for refund
```

### Visual Indicators

| Type | Color | Symbol | Example |
|------|-------|--------|---------|
| Income | 🟢 Green | + | +₹5000 |
| Expense | 🔴 Red | - | -₹500 |

### Where You'll See It

1. **Dashboard**: Recent transactions with color coding
2. **Transactions Page**: Full list with income/expense labels
3. **Balance Calculation**: Income - Expenses = Balance

---

## 📊 Balance Breakdown

### Dashboard Display

```
┌─────────────────────────────────────┐
│ Total Balance:    ₹4,500           │ (Income - Expenses)
│ Total Income:     ₹5,000 (green)   │
│ Total Expenses:   ₹500 (red)       │
└─────────────────────────────────────┘
```

### Calculation Logic

```
Income:    ₹5,000 (salary)
         + ₹200 (refund)
         = ₹5,200 total income

Expenses:  ₹500 (groceries)
         + ₹100 (transport)
         = ₹600 total expenses

Balance = ₹5,200 - ₹600 = ₹4,600
```

---

## ⚠️ Overspending Alert System

### Dashboard Alert

When any envelope is overspent, you'll see:

```
┌─────────────────────────────────────────┐
│ ⚠️ Overspending Alert!                  │
│ Groceries (₹50 over), Entertainment     │
│ (₹100 over)                             │
└─────────────────────────────────────────┘
```

### Envelope Page Indicators

**Normal Spending** (< 80%):
```
┌─────────────────────┐
│ Groceries          │
│ Allocated: ₹500    │
│ Spent: ₹300        │
│ [████████░░] 60%   │ (Blue bar)
└─────────────────────┘
```

**Warning** (80-100%):
```
┌─────────────────────┐
│ Entertainment      │
│ Allocated: ₹200    │
│ Spent: ₹180        │
│ [█████████░] 90%   │ (Yellow bar)
└─────────────────────┘
```

**Overspent** (> 100%):
```
┌─────────────────────────────┐
│ Dining Out                 │ (Red border)
│ Allocated: ₹300            │
│ Spent: ₹350                │
│ [██████████] 100%          │ (Red bar)
│ ⚠️ Overspent by ₹50        │
└─────────────────────────────┘
```

---

## 🎯 Quick Actions

### Add Income
1. Click "Add Transaction"
2. Enter merchant: "Salary"
3. Enter amount: **5000** (positive)
4. Select category: "Income"
5. Click "Add"
6. ✅ Shows in green with + symbol

### Add Expense
1. Click "Add Transaction"
2. Enter merchant: "Grocery Store"
3. Enter amount: **-500** (negative)
4. Select category: "Food & Dining"
5. Click "Add"
6. ✅ Shows in red with - symbol

### Create Budget Envelope
1. Go to "Envelopes" page
2. Click "Create Envelope"
3. Enter name: "Groceries"
4. Enter allocated: 5000
5. Click "Create"
6. ✅ Track spending against this budget

### Monitor Overspending
1. Check dashboard for red alert
2. Go to "Envelopes" page
3. Look for red-bordered envelopes
4. See exact overspending amount
5. Adjust budget or reduce spending

---

## 🎨 Theme Comparison

### Light Theme (Default)
- White backgrounds
- Dark text
- Bright, clean look
- Best for: Daytime, bright rooms

### Dark Theme
- Dark backgrounds (#1a1a1a)
- Light text (#e5e5e5)
- Reduced eye strain
- Best for: Night-time, dark rooms

**Toggle anytime** - No need to reload page!

---

## 📱 Responsive Design

All features work on:
- 💻 Desktop computers
- 📱 Mobile phones
- 📱 Tablets
- 🖥️ Large screens

Theme preference syncs across all devices (same browser).

---

## 🔢 Number Format Examples

| You Enter | System Shows | Meaning |
|-----------|--------------|---------|
| -50 | -₹50.00 (red) | Spent ₹50 |
| 1000 | +₹1,000.00 (green) | Received ₹1000 |
| -1500.50 | -₹1,500.50 (red) | Spent ₹1500.50 |
| 5000 | +₹5,000.00 (green) | Received ₹5000 |

---

## 💡 Pro Tips

1. **Use Categories Wisely**
   - "Income" category for all earnings
   - Specific categories for expenses

2. **Monitor Dashboard Daily**
   - Quick glance at balance
   - Spot overspending alerts
   - Track recent transactions

3. **Set Realistic Budgets**
   - Review past spending
   - Add 10-20% buffer
   - Adjust monthly

4. **Color Coding Benefits**
   - Quick visual scan
   - Green = Good (income)
   - Red = Watch (expenses)
   - Yellow = Warning (near limit)

5. **Dark Theme for Night**
   - Reduces blue light
   - Easier on eyes
   - Better battery life (OLED screens)

---

## 🆘 Troubleshooting

**Q: Balance seems wrong?**
A: Check if you entered expenses as negative numbers

**Q: Theme doesn't save?**
A: Make sure browser allows localStorage

**Q: No overspending alert?**
A: Alert only shows when envelope.spent > envelope.allocated

**Q: Can't see dark theme changes?**
A: Refresh the page (F5 or Ctrl+R)

**Q: Progress bar shows 0%?**
A: Check if allocated amount is greater than 0

---

## 📞 Quick Reference Card

```
┌─────────────────────────────────────┐
│ QUICK REFERENCE                     │
├─────────────────────────────────────┤
│ Toggle Theme:    🌓 (top right)     │
│ Add Income:      Positive number    │
│ Add Expense:     Negative number    │
│ Check Balance:   Dashboard          │
│ View Alerts:     Dashboard (red)    │
│ Monitor Budget:  Envelopes page     │
└─────────────────────────────────────┘
```

---

**Remember**: 
- Green = Income = Good 🟢
- Red = Expense = Monitor 🔴
- Yellow = Warning = Careful 🟡
