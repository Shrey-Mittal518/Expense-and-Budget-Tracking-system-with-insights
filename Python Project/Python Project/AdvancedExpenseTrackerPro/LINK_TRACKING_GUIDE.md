# Link-Based Purchase Tracking - Complete Guide

## Overview

The Link Tracking feature allows you to track purchases made through offer links on the site. When you click on an offer, the system:
1. Records the click
2. Adds the item to your cart
3. Creates a detected transaction for review
4. Optionally redirects you to the merchant site

## How It Works

### Step 1: Browse Offers
- Go to the **Offers** page
- Browse live offers from popular shopping sites
- Each offer has an "Add to Cart 🛒" button

### Step 2: Click to Track
- Click "Add to Cart" on any offer
- System records your click
- Item added to session cart (cart icon updates)
- You're redirected to the merchant site (or see confirmation page)

### Step 3: Complete Purchase
- Complete your purchase on the merchant site
- Return to the expense tracker app

### Step 4: Review & Accept
- Go to **Cart** page
- See your clicked items in "Detected Transactions"
- Click "Accept" to add to your transaction history
- Click "Reject" to remove items you didn't purchase

## Features

### 🛒 Shopping Cart

**Location:** Cart icon in top navigation bar

**What it shows:**
- Number of items clicked (badge)
- Session cart items
- Detected transactions pending review

**Actions:**
- View cart details
- Clear cart
- Accept/reject transactions

### 📦 Detected Transactions

**Confidence Levels:**
- **High (Green):** Known merchant + amount specified
- **Medium (Yellow):** Known merchant OR amount specified
- **Low (Red):** Unknown merchant and no amount

**Information Displayed:**
- Merchant name
- Confidence badge
- Online sale badge
- Category and date
- Amount (if known)

### 🔗 Tracking Links

**How they work:**
- Each offer gets a unique tracking ID (UUID)
- Format: `/track/<tracking_id>`
- Clicking records metadata:
  - User ID (if logged in)
  - IP address
  - User agent
  - Referrer
  - Timestamp

### 🔒 Safe Redirects

**Security Features:**
- Only HTTPS URLs allowed
- Domain whitelist validation
- No open redirect vulnerabilities
- XSS prevention

**Whitelisted Domains:**
- amazon.in, amazon.com
- flipkart.com
- myntra.com
- swiggy.com
- zomato.com
- paytm.com
- And more (see `config/safe_domains.txt`)

## User Workflows

### Workflow 1: Standard Purchase

```
1. Browse Offers page
2. Click "Add to Cart" on Amazon offer
3. Redirected to Amazon
4. Complete purchase on Amazon
5. Return to app
6. Go to Cart page
7. See detected transaction
8. Click "Accept"
9. Transaction added to history
```

### Workflow 2: Browse Without Redirect

```
1. Browse Offers page
2. Right-click "Add to Cart"
3. Copy link and add ?redirect=false
4. Visit modified URL
5. See "Added to Cart" confirmation page
6. Choose to continue to merchant or browse more
```

### Workflow 3: Review Later

```
1. Click multiple offers throughout the day
2. Cart icon shows count (e.g., 5)
3. At end of day, go to Cart
4. Review all detected transactions
5. Accept purchases you made
6. Reject items you didn't buy
```

## Cart Page Sections

### 1. Cart Statistics
- **Total Clicks:** All tracking links clicked
- **Accepted Purchases:** Transactions you've accepted
- **Unique Items:** Distinct products clicked

### 2. Current Session Cart
- Items clicked in current session
- Shows: Title, Merchant, Amount, Timestamp
- "Clear Cart" button to empty session

### 3. Detected Transactions
- Pending transactions for review
- Shows: Merchant, Confidence, Amount, Category
- Accept/Reject buttons for each

## Technical Details

### Database Tables

**link_tracking:**
```sql
tracking_id TEXT PRIMARY KEY
merchant TEXT
title TEXT
amount REAL
target_url TEXT
offer_id INTEGER
created_by_user INTEGER
created_at TIMESTAMP
```

**link_clicks:**
```sql
id INTEGER PRIMARY KEY
tracking_id TEXT
user_id INTEGER (nullable for anonymous)
ip TEXT
user_agent TEXT
referer TEXT
timestamp TIMESTAMP
accepted_flag INTEGER (0 or 1)
extra_meta TEXT
```

### Transaction Log Format

When you accept a detected transaction, it's appended to `data/users/<user_id>.txt`:

```
2025-11-10 12:00:00 | -1000.00 | Amazon | Shopping | source=link | tracking_id=550e8400...
```

### Confidence Calculation

```python
if known_merchant and has_amount:
    confidence = 'High'
elif known_merchant or has_amount:
    confidence = 'Medium'
else:
    confidence = 'Low'
```

## Configuration

### Enable/Disable Redirect

**Default:** Redirect enabled

**To disable for a specific link:**
Add `?redirect=false` to tracking URL:
```
/track/550e8400-e29b-41d4-a716-446655440000?redirect=false
```

### Manage Safe Domains

**File:** `config/safe_domains.txt`

**To add a domain:**
1. Open `config/safe_domains.txt`
2. Add domain (one per line)
3. Restart application

**Example:**
```
amazon.in
flipkart.com
mynewstore.com
```

## API Endpoints

### GET /track/<tracking_id>

**Purpose:** Track click and redirect

**Parameters:**
- `redirect` (query): "1" (default) or "0"

**Response:**
- Redirect to merchant (if redirect=1)
- Confirmation page (if redirect=0)

**Side Effects:**
- Records click in database
- Adds item to session cart
- Creates detected transaction (if logged in)

### GET /cart

**Purpose:** View cart and detected transactions

**Requires:** Login

**Response:** Cart page with:
- Session cart items
- Detected transactions
- Statistics

### POST /cart/accept-detected/<detected_id>

**Purpose:** Accept detected transaction

**Requires:** Login

**Parameters:**
- `tracking_id` (form): Optional tracking ID

**Response:**
- Redirect to cart
- Flash message

**Side Effects:**
- Creates transaction in database
- Appends to user's .txt file
- Marks click as accepted
- Removes from detected transactions

### POST /cart/clear

**Purpose:** Clear session cart

**Requires:** Login

**Response:**
- Redirect to cart
- Flash message

**Side Effects:**
- Empties session['cart']

## Security Considerations

### 1. Open Redirect Prevention

**Risk:** Attacker creates tracking link to malicious site

**Mitigation:**
- Whitelist of safe domains
- HTTPS-only validation
- URL parsing and validation

### 2. XSS Prevention

**Risk:** Malicious merchant name with script tags

**Mitigation:**
- Jinja2 auto-escaping
- HTML entity encoding
- Input sanitization

### 3. SQL Injection

**Risk:** Malicious tracking_id in URL

**Mitigation:**
- Parameterized queries
- UUID validation
- Input validation

### 4. CSRF Protection

**Risk:** External site triggers accept action

**Mitigation:**
- Flask CSRF tokens (if enabled)
- Session validation
- Referer checking

### 5. Session Hijacking

**Risk:** Attacker steals session cookie

**Mitigation:**
- Secure session cookies
- HTTPOnly flag
- Session timeout

## Troubleshooting

### Issue: Cart count not updating

**Solution:**
- Refresh page
- Check browser console for errors
- Verify JavaScript enabled

### Issue: Redirect not working

**Solution:**
- Check if domain is whitelisted
- Verify URL is HTTPS
- Check `config/safe_domains.txt`

### Issue: Detected transaction not appearing

**Solution:**
- Ensure you're logged in
- Check if amount was specified
- Verify click was recorded (check database)

### Issue: Accept button not working

**Solution:**
- Check for error messages
- Verify user permissions
- Check database connectivity

### Issue: Anonymous clicks not tracked

**Solution:**
- This is expected behavior
- Log in to create detected transactions
- Session cart still works when logged out

## Best Practices

### For Users

1. **Review Regularly:** Check cart daily to accept/reject
2. **Clear Cart:** Clear session cart after reviewing
3. **Verify Amounts:** Check detected amounts match actual purchases
4. **Report Issues:** Report suspicious tracking links

### For Administrators

1. **Monitor Whitelist:** Regularly review safe domains
2. **Check Logs:** Monitor click patterns for abuse
3. **Update Security:** Keep dependencies updated
4. **Backup Data:** Regular backups of tracking data
5. **Review Analytics:** Analyze click-through rates

## Analytics & Insights

### Available Metrics

- Total clicks per user
- Accepted vs rejected transactions
- Unique items clicked
- Click-through rate by merchant
- Conversion rate (clicks to accepted)

### Future Analytics

- Popular offers
- Peak clicking times
- Merchant performance
- User engagement metrics
- Revenue tracking (if amounts known)

## Privacy Considerations

### Data Collected

- Click timestamp
- IP address
- User agent
- Referrer URL
- User ID (if logged in)

### Data Usage

- Track purchase behavior
- Improve offer recommendations
- Detect fraud/abuse
- Generate analytics

### Data Retention

- Clicks: Retained indefinitely
- Session cart: Cleared on logout
- Detected transactions: Until accepted/rejected

### User Rights

- View all tracked clicks
- Delete tracking data (on request)
- Opt-out of tracking (don't click links)
- Export tracking data

## FAQ

**Q: Do I have to accept every detected transaction?**
A: No, only accept purchases you actually made.

**Q: What if I clicked by mistake?**
A: Just reject the detected transaction or clear your cart.

**Q: Can I track purchases from any website?**
A: Only whitelisted domains are supported for security.

**Q: What happens if I click the same offer twice?**
A: Both clicks are recorded, but you should only accept once.

**Q: Can I see my click history?**
A: Yes, go to Cart page to see recent clicks and statistics.

**Q: Is my data secure?**
A: Yes, we use industry-standard security practices.

**Q: Can I disable tracking?**
A: Yes, simply don't click the tracking links.

**Q: What if the amount is wrong?**
A: You can edit the transaction after accepting it.

**Q: Can I track offline purchases?**
A: No, this feature is for online purchases only.

**Q: How long does data stay in my cart?**
A: Session cart clears on logout; detected transactions stay until accepted/rejected.

## Support

For issues or questions:
1. Check this guide
2. Review TEST_PLAN.md
3. Check PROJECT_TASKS.md for known issues
4. Contact support

---

**Version:** 1.0  
**Last Updated:** November 10, 2025  
**Status:** Production Ready
