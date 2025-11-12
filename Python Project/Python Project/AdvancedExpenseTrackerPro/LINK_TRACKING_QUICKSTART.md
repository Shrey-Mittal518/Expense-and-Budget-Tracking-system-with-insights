# Link Tracking - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Browse Offers
```
Go to: Offers page
Look for: "Add to Cart 🛒" buttons
```

### Step 2: Click to Track
```
Click: Any "Add to Cart" button
Result: Item added to cart, redirected to merchant
```

### Step 3: Accept Purchase
```
Go to: Cart page
Action: Click "Accept" on detected transactions
Result: Transaction added to your history
```

## 📊 Quick Reference

### Cart Icon
- **Location:** Top navigation bar (🛒)
- **Shows:** Number of items in cart
- **Click:** Opens cart page

### Detected Transactions
- **Green Badge:** High confidence
- **Yellow Badge:** Medium confidence
- **Red Badge:** Low confidence

### Actions
- **Accept:** Add to transaction history
- **Reject:** Remove from cart
- **Clear Cart:** Empty session cart

## 🔗 URL Parameters

### Enable Redirect (default)
```
/track/<tracking_id>
```

### Disable Redirect
```
/track/<tracking_id>?redirect=false
```

## 🛠️ For Developers

### Run Tests
```bash
pytest tests/test_link_tracking.py -v
```

### Check Database
```sql
SELECT * FROM link_tracking;
SELECT * FROM link_clicks;
```

### Add Safe Domain
```bash
echo "newstore.com" >> config/safe_domains.txt
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `services/link_tracker.py` | Core tracking logic |
| `templates/cart.html` | Cart page |
| `templates/added_to_cart.html` | Confirmation page |
| `config/safe_domains.txt` | Whitelist |
| `tests/test_link_tracking.py` | Unit tests |

## 🔒 Security

### Safe Redirects Only
- ✅ HTTPS required
- ✅ Whitelisted domains
- ❌ No open redirects
- ❌ No XSS

### Data Protection
- User data isolated
- Parameterized queries
- Session validation
- Input sanitization

## 💡 Tips

1. **Check cart regularly** - Review detected transactions daily
2. **Accept only real purchases** - Reject accidental clicks
3. **Clear cart after review** - Keep cart clean
4. **Report issues** - Contact support for problems

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Cart not updating | Refresh page |
| Redirect failing | Check whitelist |
| Accept not working | Check login status |
| Tests failing | Check database |

## 📞 Need Help?

1. Read `LINK_TRACKING_GUIDE.md`
2. Check `TEST_PLAN.md`
3. Review `LINK_TRACKING_IMPLEMENTATION.md`
4. Contact support

---

**Quick Links:**
- [Full Guide](LINK_TRACKING_GUIDE.md)
- [Test Plan](TEST_PLAN.md)
- [Implementation](LINK_TRACKING_IMPLEMENTATION.md)
