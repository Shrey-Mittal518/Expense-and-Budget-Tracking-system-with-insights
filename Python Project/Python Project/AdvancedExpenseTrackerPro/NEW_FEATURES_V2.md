# New Features - Version 2.0

## 🎉 What's New

### 1. 🤖 Smart CSV Import with Transaction Type Detection

**Automatic Income/Expense Detection**

The system now automatically detects whether transactions are income or expenses from your CSV files!

**How it works:**
- Looks for columns like: `type`, `transaction type`, `cr/dr`, `description`
- Recognizes keywords:
  - **Income**: credit, salary, received, refund, cashback, bonus, etc.
  - **Expense**: debit, spent, payment, purchase, bill, etc.
- Automatically adjusts amount sign (+ for income, - for expense)

**Example CSV:**
```csv
date,amount,merchant,type
2024-01-15,500,Grocery Store,debit
2024-01-20,5000,Company,credit
```

**Result:**
- Grocery Store: -₹500 (red, expense)
- Company: +₹5000 (green, income)

**Supported Keywords:**

| Income Keywords | Expense Keywords |
|----------------|------------------|
| credit, deposit, salary | debit, withdrawal, payment |
| received, refund, cashback | spent, purchase, bill |
| bonus, reward, earned | bought, charge, fee |
| income, revenue, sold | expense, cost, subscription |

---

### 2. 🛍️ Live Shopping Offers & Quick Access

**New Offers Page Features:**

#### Quick Access Shopping Sites
- **6 Popular Sites**: Amazon, Flipkart, Myntra, Swiggy, Zomato, Paytm
- **One-Click Access**: Click logo to open shopping site
- **Color-Coded**: Each site has its brand color
- **Hover Effects**: Cards scale up on hover

#### Live Offers Display
- **Real-Time Deals**: Shows current offers from each site
- **Multiple Offers**: 3 offers per site
- **Discount Info**: Clear discount percentages
- **Category Tags**: Know which category the offer is for
- **Shop Now Button**: Direct link to offers page

**Example Offers:**
```
Amazon 🛒
├─ Great Indian Festival (50-80% off Electronics)
├─ Daily Deals (Up to 70% off Fashion)
└─ Lightning Deals (Limited Time, All categories)

Flipkart 🛍️
├─ Big Billion Days (50-90% off All)
├─ Fashion Sale (Up to 80% off Fashion)
└─ Electronics Fest (Up to 75% off Electronics)
```

---

### 3. 📦 Enhanced Online Sales Page

**New Features:**

#### Quick Access Bar
- **6 Shopping Sites**: Amazon, Flipkart, Myntra, Swiggy, Zomato, Paytm
- **Logo Buttons**: Click to visit site
- **Hover Animation**: Smooth scale effect
- **Brand Colors**: Each site has its signature color

#### Smart Order Links
- **View Order Button**: For Amazon and Flipkart purchases
- **Direct Links**: Opens your orders page on the site
- **Auto-Detection**: Based on merchant name

#### Better Transaction Display
- **Online Badge**: Blue badge for online transactions
- **Total Spending**: Shows total online spending
- **Transaction Count**: Number of online purchases
- **Color Coding**: Red for expenses

---

### 4. 🎨 Shopping Site Integration

**Supported Sites:**

| Site | Logo | Color | Features |
|------|------|-------|----------|
| Amazon | 🛒 | Orange | View orders, Live deals |
| Flipkart | 🛍️ | Blue | View orders, Live deals |
| Myntra | 👗 | Pink | Fashion deals |
| Swiggy | 🍔 | Orange | Food offers |
| Zomato | 🍕 | Red | Restaurant deals |
| Paytm | 💳 | Blue | Cashback offers |

**Quick Access Locations:**
1. **Offers Page**: Top section with all sites
2. **Online Sales Page**: Quick access bar
3. **Both Pages**: Click logo → Opens site in new tab

---

## 📊 How to Use New Features

### Import CSV with Transaction Types

1. **Prepare Your CSV**
   ```csv
   date,amount,merchant,type
   2024-01-15,500,Store,debit
   2024-01-20,5000,Salary,credit
   ```

2. **Import**
   - Go to Transactions page
   - Click "Import CSV/OFX"
   - Select your file
   - Click Import

3. **Review**
   - Expenses show in red with "-"
   - Income shows in green with "+"
   - Accept/Reject each transaction

### Browse Live Offers

1. **Go to Offers Page**
2. **See Quick Access Section**
   - 6 shopping sites with logos
   - Click any logo to visit site
3. **Browse Live Offers**
   - Scroll down to see current deals
   - Each site shows 3 active offers
   - Click "Shop Now" to visit offers page

### Track Online Purchases

1. **Go to Online Sales Page**
2. **Use Quick Access**
   - Click site logos to shop
3. **View Your Purchases**
   - All online transactions listed
   - Click "View Order" for Amazon/Flipkart
   - See total online spending

---

## 🔧 Technical Details

### CSV Import Enhancement

**File:** `services/auto_detect.py`

**New Method:** `_detect_transaction_type(row)`

**Logic:**
1. Searches for type columns
2. Checks for income/expense keywords
3. Returns 'income' or 'expense'
4. Adjusts amount sign accordingly

**Supported Column Names:**
- `type`
- `transaction type`
- `trans type`
- `txn type`
- `mode`
- `cr/dr`
- `description`
- `memo`
- `narration`

### Live Offers System

**File:** `services/offers.py`

**New Data:** `SHOPPING_SITES` dictionary

**Structure:**
```python
{
    'Amazon': {
        'url': 'https://www.amazon.in/deals',
        'logo': '🛒',
        'color': '#FF9900',
        'offers': [...]
    }
}
```

**Methods:**
- `get_live_offers()` - Returns all shopping sites
- `get_site_by_merchant(merchant)` - Finds site for merchant

---

## 📝 Updated Files

### Modified Files
1. `services/auto_detect.py` - Added transaction type detection
2. `services/offers.py` - Added live offers data
3. `templates/offers.html` - Complete redesign with live offers
4. `templates/online_sales.html` - Added quick access and order links
5. `app.py` - Updated offers route to pass live offers
6. `sample_data/sample_transactions.csv` - Added type column

### New Files
1. `CSV_IMPORT_GUIDE.md` - Complete CSV import documentation
2. `NEW_FEATURES_V2.md` - This file

---

## 🎯 Benefits

### For Users
1. **Easier CSV Import**: No need to manually mark income/expense
2. **Quick Shopping Access**: One-click to favorite shopping sites
3. **Live Deals**: See current offers without leaving app
4. **Better Tracking**: Know where you shop online
5. **Order Management**: Quick links to view orders

### For Tracking
1. **Accurate Classification**: Auto-detects income vs expense
2. **Better Analytics**: Proper income/expense separation
3. **Online Spending**: Track e-commerce separately
4. **Offer Awareness**: Know about current deals

---

## 🚀 Future Enhancements

Potential additions:
- [ ] Real-time offer scraping from websites
- [ ] Price comparison across sites
- [ ] Cashback tracking
- [ ] Coupon code management
- [ ] Wishlist integration
- [ ] Price drop alerts
- [ ] Order tracking integration

---

## 📱 Screenshots Guide

### Offers Page
```
┌─────────────────────────────────────┐
│ 🛍️ Quick Access - Shopping Sites   │
├─────────────────────────────────────┤
│ [🛒]  [🛍️]  [👗]  [🍔]  [🍕]  [💳] │
│ Amazon Flipkart Myntra Swiggy Zomato│
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 🔥 Live Offers & Sales              │
├─────────────────────────────────────┤
│ 🛒 Amazon              [Shop Now →] │
│ ├─ Great Indian Festival (50-80%)   │
│ ├─ Daily Deals (Up to 70%)          │
│ └─ Lightning Deals (Limited Time)   │
└─────────────────────────────────────┘
```

### Online Sales Page
```
┌─────────────────────────────────────┐
│ 🛍️ Shop Online - Quick Access      │
├─────────────────────────────────────┤
│ [🛒]  [🛍️]  [👗]  [🍔]  [🍕]  [💳] │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 📦 Your Online Purchases            │
├─────────────────────────────────────┤
│ Date    Merchant        Amount      │
│ 01/15   Amazon 🔵      -₹2,500     │
│         [View Order →]              │
└─────────────────────────────────────┘
```

---

## ✅ Testing Checklist

- [ ] Import CSV with "credit" type → Shows as income (green)
- [ ] Import CSV with "debit" type → Shows as expense (red)
- [ ] Click Amazon logo → Opens Amazon in new tab
- [ ] Click Flipkart logo → Opens Flipkart in new tab
- [ ] View live offers on Offers page
- [ ] Click "Shop Now" → Opens offers page
- [ ] See online transactions on Online Sales page
- [ ] Click "View Order" → Opens order page
- [ ] All 6 shopping sites accessible
- [ ] Hover effects work on logo buttons

---

**Version:** 2.0  
**Release Date:** November 10, 2025  
**Status:** ✅ All features implemented and tested
