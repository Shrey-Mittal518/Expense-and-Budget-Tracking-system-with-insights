# Envelope Allocation Guide

## Overview

You can now allocate funds from your main balance directly to envelopes! This makes budget management easier and more flexible.

## Two Ways to Manage Envelope Funds

### 1. 💰 Allocate from Balance

**What it does:**
- Takes money from your main balance
- Adds it to an envelope's allocated amount
- Helps you set aside money for specific purposes

**How to use:**
1. Go to **Envelopes** page
2. See your **Available Balance** at the top
3. Select which envelope to allocate to
4. Enter amount
5. Click **Allocate Funds**

**Example:**
```
Available Balance: ₹10,000

Allocate ₹2,000 to "Groceries" envelope
→ Groceries envelope now has ₹2,000 allocated
→ Your balance remains ₹10,000 (allocation doesn't deduct from balance)
```

**Important Notes:**
- ✅ System checks if you have sufficient balance
- ✅ Cannot allocate more than available balance
- ✅ Allocation increases envelope's budget
- ✅ Helps you plan spending in advance

### 2. 🔄 Transfer Between Envelopes

**What it does:**
- Moves allocated funds from one envelope to another
- Useful when you need to adjust budgets
- Doesn't affect your main balance

**How to use:**
1. Go to **Envelopes** page
2. Scroll to "Transfer Between Envelopes"
3. Select **From Envelope**
4. Select **To Envelope**
5. Enter amount
6. Click **Transfer**

**Example:**
```
Groceries: ₹5,000 allocated
Entertainment: ₹1,000 allocated

Transfer ₹500 from Groceries to Entertainment
→ Groceries: ₹4,500 allocated
→ Entertainment: ₹1,500 allocated
```

## Visual Guide

### Envelopes Page Layout

```
┌─────────────────────────────────────────┐
│ Budget Envelopes                        │
├─────────────────────────────────────────┤
│ [Envelope Cards Display]                │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 💰 Allocate from Balance                │
├─────────────────────────────────────────┤
│ Available Balance: ₹10,000              │
│                                         │
│ [Select Envelope ▼] [Amount] [Allocate]│
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 🔄 Transfer Between Envelopes           │
├─────────────────────────────────────────┤
│ [From ▼] [To ▼] [Amount] [Transfer]    │
└─────────────────────────────────────────┘
```

## Use Cases

### Use Case 1: Monthly Budget Setup

**Scenario:** You just received your salary

**Steps:**
1. Salary of ₹50,000 credited (shows as income)
2. Go to Envelopes page
3. Allocate funds:
   - ₹10,000 to Groceries
   - ₹5,000 to Entertainment
   - ₹3,000 to Transportation
   - ₹2,000 to Healthcare

**Result:** You've budgeted ₹20,000 for specific purposes

### Use Case 2: Budget Adjustment

**Scenario:** You overspent on groceries, need to adjust

**Steps:**
1. Groceries envelope: ₹10,000 allocated, ₹12,000 spent (overspent!)
2. Entertainment envelope: ₹5,000 allocated, ₹2,000 spent (underspent)
3. Transfer ₹2,000 from Entertainment to Groceries

**Result:** Balanced your budget without adding new money

### Use Case 3: Emergency Allocation

**Scenario:** Unexpected medical expense

**Steps:**
1. Check available balance: ₹15,000
2. Create new envelope "Medical Emergency"
3. Allocate ₹5,000 from balance
4. Add medical expense transaction to this envelope

**Result:** Emergency handled with proper tracking

## Balance vs Allocation

### Understanding the Difference

**Balance:**
- Your actual money (income - expenses)
- Shows how much you have
- Changes with every transaction

**Allocation:**
- How you plan to use your money
- Shows your budget for each category
- Changes when you allocate or transfer

**Example:**
```
Balance: ₹10,000 (actual money you have)

Allocations:
├─ Groceries: ₹3,000 (planned spending)
├─ Entertainment: ₹2,000 (planned spending)
└─ Savings: ₹5,000 (planned saving)
Total Allocated: ₹10,000

Note: You can allocate up to your balance amount
```

## Validation & Safety

### System Checks

1. **Sufficient Balance Check**
   - Cannot allocate more than available balance
   - Error message shows available amount

2. **Same Envelope Check**
   - Cannot transfer to the same envelope
   - Error message displayed

3. **Sufficient Allocation Check**
   - Cannot transfer more than envelope has
   - Prevents negative allocations

### Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "Insufficient balance" | Not enough money | Add income or reduce amount |
| "Cannot transfer to same envelope" | From and To are same | Select different envelopes |
| "Insufficient funds in envelope" | Source envelope doesn't have enough | Reduce amount or choose different source |

## Best Practices

### 1. Plan Your Budget Monthly

```
Start of Month:
1. Check total balance
2. List all expenses for the month
3. Create/update envelopes
4. Allocate funds to each envelope
5. Track spending throughout month
```

### 2. Use Descriptive Envelope Names

✅ Good Names:
- "Monthly Groceries"
- "Entertainment & Dining"
- "Emergency Fund"
- "Rent & Utilities"

❌ Avoid:
- "Envelope 1"
- "Misc"
- "Other"

### 3. Review and Adjust Weekly

- Check which envelopes are overspent
- Transfer funds if needed
- Adjust allocations for next month

### 4. Keep Some Unallocated

```
Total Balance: ₹50,000
Allocated: ₹40,000
Unallocated: ₹10,000 (buffer for unexpected expenses)
```

## Quick Reference

### Allocate from Balance
```
Purpose: Set aside money for specific category
When: Start of month, after receiving income
Effect: Increases envelope allocation
Balance: Doesn't change
```

### Transfer Between Envelopes
```
Purpose: Adjust budget between categories
When: Mid-month, when needs change
Effect: Moves allocation from one to another
Balance: Doesn't change
```

## Keyboard Shortcuts

- **Tab**: Move between fields
- **Enter**: Submit form
- **Esc**: Close modals (if any)

## Mobile Usage

On mobile devices:
- Forms stack vertically
- All fields remain accessible
- Touch-friendly buttons
- Responsive layout

## Troubleshooting

**Q: Why can't I allocate ₹5,000 when my balance is ₹10,000?**
A: Check if you already have allocations. Total allocations cannot exceed balance.

**Q: I allocated money but my balance didn't decrease?**
A: Correct! Allocation is planning, not spending. Balance decreases only when you add expense transactions.

**Q: Can I allocate to multiple envelopes at once?**
A: Currently, allocate one at a time. Repeat the process for each envelope.

**Q: What happens if I delete an envelope with allocated funds?**
A: The allocated amount is released back to your available balance.

## Tips & Tricks

1. **Zero-Based Budgeting**
   - Allocate every rupee of your balance
   - Ensures all money has a purpose

2. **Percentage Allocation**
   - 50% Needs (groceries, rent, utilities)
   - 30% Wants (entertainment, dining)
   - 20% Savings (emergency fund, goals)

3. **Color Coding**
   - Use envelope names with emojis
   - 🍔 Food & Dining
   - 🎬 Entertainment
   - 🏥 Healthcare

4. **Regular Reviews**
   - Weekly: Check spending vs allocation
   - Monthly: Adjust allocations
   - Quarterly: Review overall budget strategy

---

**Pro Tip:** Start with broad categories and refine as you learn your spending patterns!
