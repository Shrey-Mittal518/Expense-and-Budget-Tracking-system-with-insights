# Link Tracking Feature - Test Plan

## Overview
This document describes how to validate the end-to-end link-based purchase tracking functionality.

## Prerequisites
- Application running on http://localhost:8000
- User account created and logged in
- pytest installed (`pip install pytest`)

## Unit Tests

### Run All Tests
```bash
cd AdvancedExpenseTrackerPro
pytest tests/test_link_tracking.py -v
```

### Expected Results
All tests should pass:
- ✅ test_create_tracking_link
- ✅ test_get_tracked_item
- ✅ test_record_click
- ✅ test_anonymous_click
- ✅ test_is_safe_redirect_valid
- ✅ test_is_safe_redirect_invalid
- ✅ test_calculate_confidence_high
- ✅ test_calculate_confidence_medium
- ✅ test_calculate_confidence_low
- ✅ test_mark_click_accepted
- ✅ test_get_click_stats
- ✅ test_multiple_clicks_same_item

## End-to-End Testing

### Test Case 1: View Offers with Tracking Links

**Steps:**
1. Log in to the application
2. Navigate to "Offers" page
3. Observe the live offers section

**Expected Results:**
- Each offer has an "Add to Cart 🛒" button
- Buttons are clickable
- No console errors

**Pass Criteria:** ✅ All offers display tracking buttons

---

### Test Case 2: Click Tracking Link (With Redirect)

**Steps:**
1. Go to Offers page
2. Click "Add to Cart" on any offer
3. Observe behavior

**Expected Results:**
- Flash message appears: "Item added to cart"
- Cart icon in navbar shows count (1)
- User is redirected to merchant website
- New tab/window opens with merchant site

**Pass Criteria:** ✅ Redirect works and cart updates

---

### Test Case 3: Click Tracking Link (Without Redirect)

**Steps:**
1. Go to Offers page
2. Right-click "Add to Cart" button
3. Copy link address
4. Paste in browser and add `?redirect=false` to URL
5. Press Enter

**Expected Results:**
- "Added to Cart" confirmation page appears
- Shows item details (merchant, title, amount)
- Provides options:
  - Continue to merchant
  - View Cart
  - Browse More Offers

**Pass Criteria:** ✅ Confirmation page displays correctly

---

### Test Case 4: View Shopping Cart

**Steps:**
1. After clicking some offers, go to Cart page
2. Observe cart contents

**Expected Results:**
- Cart statistics show:
  - Total Clicks
  - Accepted Purchases
  - Unique Items
- Session cart shows clicked items with:
  - Title
  - Merchant
  - Amount
  - Timestamp
- "Clear Cart" button visible

**Pass Criteria:** ✅ Cart displays all clicked items

---

### Test Case 5: View Detected Transactions

**Steps:**
1. Go to Cart page
2. Scroll to "Detected Transactions" section

**Expected Results:**
- Shows items pending review
- Each item displays:
  - Merchant name
  - Confidence badge (High/Medium/Low)
  - Online badge
  - Category and date
  - Amount
  - Accept/Reject buttons

**Pass Criteria:** ✅ Detected transactions appear correctly

---

### Test Case 6: Accept Detected Transaction

**Steps:**
1. In Cart page, find a detected transaction
2. Click "Accept" button
3. Observe results

**Expected Results:**
- Flash message: "Transaction accepted and added to your records"
- Item removed from detected transactions
- Item appears in Transactions page
- Entry appended to `data/users/<user_id>.txt`
- Cart statistics update (Accepted Purchases +1)

**Pass Criteria:** ✅ Transaction accepted and persisted

---

### Test Case 7: Reject Detected Transaction

**Steps:**
1. In Cart page, find a detected transaction
2. Click "Reject" button

**Expected Results:**
- Item removed from detected transactions
- No transaction created
- Flash message confirms rejection

**Pass Criteria:** ✅ Transaction rejected successfully

---

### Test Case 8: Clear Cart

**Steps:**
1. Add multiple items to cart
2. Go to Cart page
3. Click "Clear Cart" button

**Expected Results:**
- Session cart emptied
- Cart count in navbar shows 0
- Flash message: "Cart cleared"
- Detected transactions remain (not cleared)

**Pass Criteria:** ✅ Session cart cleared

---

### Test Case 9: Anonymous Click (Logged Out)

**Steps:**
1. Log out of application
2. Manually visit a tracking URL: `/track/<tracking_id>`
3. Observe behavior

**Expected Results:**
- Click is recorded with user_id=NULL
- Item added to session cart
- Redirect works (if enabled)
- No detected transaction created (requires login)

**Pass Criteria:** ✅ Anonymous tracking works

---

### Test Case 10: Multiple Clicks Same Item

**Steps:**
1. Click same offer 3 times
2. Go to Cart page

**Expected Results:**
- Session cart shows 3 entries (same item)
- Click statistics show 3 total clicks
- Only 1 unique item

**Pass Criteria:** ✅ Multiple clicks tracked correctly

---

### Test Case 11: Cart Icon Updates

**Steps:**
1. Note cart count in navbar (e.g., 0)
2. Click an offer
3. Observe cart icon

**Expected Results:**
- Cart count increments immediately
- Badge shows correct number
- Badge is visible and styled (red background)

**Pass Criteria:** ✅ Cart icon updates in real-time

---

### Test Case 12: Transaction Persistence

**Steps:**
1. Accept a detected transaction
2. Check `data/users/<user_id>.txt` file
3. Verify entry format

**Expected Results:**
- New line appended to file
- Format: `timestamp | amount | merchant | category | source=link | tracking_id`
- File permissions correct
- No corruption

**Pass Criteria:** ✅ Transaction logged to file

---

### Test Case 13: Safe Redirect Validation

**Steps:**
1. Try to create tracking link with invalid URL
2. Attempt redirect to non-whitelisted domain

**Expected Results:**
- Invalid URLs rejected
- Non-HTTPS URLs rejected
- Non-whitelisted domains rejected
- Error message or fallback behavior

**Pass Criteria:** ✅ Only safe redirects allowed

---

### Test Case 14: Confidence Calculation

**Steps:**
1. Click offers from known merchants (Amazon, Flipkart)
2. Click offers with amounts specified
3. Check detected transactions

**Expected Results:**
- Known merchant + amount = High confidence (green)
- Known merchant OR amount = Medium confidence (yellow)
- Neither = Low confidence (red)

**Pass Criteria:** ✅ Confidence levels correct

---

### Test Case 15: Database Integrity

**Steps:**
1. Click multiple offers
2. Accept some, reject others
3. Check database tables

**Expected Results:**
- `link_tracking` table has entries
- `link_clicks` table records all clicks
- `detected_transactions` table updated correctly
- Foreign keys maintained
- No orphaned records

**Pass Criteria:** ✅ Database consistent

---

## Security Testing

### SEC-1: Open Redirect Prevention

**Test:**
```
/track/<id>?redirect=true
```
Where tracking link has `target_url=https://evil.com`

**Expected:** Redirect blocked, error shown

---

### SEC-2: XSS Prevention

**Test:**
Create tracking link with:
```
merchant='<script>alert(1)</script>'
```

**Expected:** Script tags escaped in HTML

---

### SEC-3: SQL Injection

**Test:**
```
/track/'; DROP TABLE link_tracking; --
```

**Expected:** 404 error, no SQL executed

---

### SEC-4: CSRF Protection

**Test:**
POST to `/cart/accept-detected/<id>` from external site

**Expected:** CSRF token validation (if implemented)

---

## Performance Testing

### PERF-1: Concurrent Clicks

**Test:**
10 users clicking offers simultaneously

**Expected:**
- All clicks recorded
- No race conditions
- Database locks handled
- Response time < 500ms

---

### PERF-2: Large Cart

**Test:**
Add 100 items to cart

**Expected:**
- Cart page loads < 2s
- No memory issues
- Pagination works (if implemented)

---

## Regression Testing

After implementing link tracking, verify:

- [ ] Existing transaction features still work
- [ ] CSV import not affected
- [ ] Envelopes functionality intact
- [ ] Goals tracking works
- [ ] Forecast calculations correct
- [ ] User authentication unchanged
- [ ] All existing tests pass

---

## Browser Compatibility

Test on:
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

---

## Acceptance Criteria Summary

✅ **Must Pass:**
1. Tracking links created for all offers
2. Clicks recorded in database
3. Cart icon updates immediately
4. Detected transactions appear in cart
5. Accept/reject functionality works
6. Transactions persisted to DB and .txt file
7. Safe redirect validation prevents attacks
8. All unit tests pass
9. No console errors
10. No security vulnerabilities

---

## Test Execution Checklist

- [ ] Run unit tests: `pytest tests/test_link_tracking.py`
- [ ] Run all tests: `pytest`
- [ ] Manual test all 15 end-to-end scenarios
- [ ] Security tests (SEC-1 through SEC-4)
- [ ] Performance tests (PERF-1, PERF-2)
- [ ] Regression tests
- [ ] Browser compatibility tests
- [ ] Review code for security issues
- [ ] Check database schema
- [ ] Verify file permissions
- [ ] Test error handling
- [ ] Test edge cases

---

## Bug Reporting Template

```
**Bug ID:** LT-XXX
**Severity:** Critical/High/Medium/Low
**Test Case:** [Test case number]
**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Result:**

**Actual Result:**

**Screenshots:**

**Environment:**
- Browser:
- OS:
- Python version:
- Flask version:
```

---

## Sign-Off

**Tested By:** _______________  
**Date:** _______________  
**Status:** Pass / Fail / Blocked  
**Notes:**

---

## Appendix: Sample Test Data

### Sample Tracking Link
```
tracking_id: 550e8400-e29b-41d4-a716-446655440000
merchant: Amazon
title: Great Indian Festival Deal
amount: 1000.00
target_url: https://amazon.in/deals
```

### Sample Click Record
```
tracking_id: 550e8400-e29b-41d4-a716-446655440000
user_id: 1
ip: 127.0.0.1
user_agent: Mozilla/5.0...
timestamp: 2025-11-10 12:00:00
```

### Sample Detected Transaction
```
user_id: 1
merchant: Amazon
amount: -1000.00
category: Shopping
confidence: High
is_online_sale: 1
```
