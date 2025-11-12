# Project Tasks & Development Roadmap

## Completed Features ✓

### Core Infrastructure
- [x] Flask application setup with proper routing
- [x] SQLite database schema and initialization
- [x] User authentication with bcrypt password hashing
- [x] Flask-Login session management
- [x] Per-user data isolation
- [x] Per-user transaction log files (.txt)

### User Management
- [x] User registration with validation
- [x] Secure login/logout
- [x] Password hashing with bcrypt
- [x] Auto-detect transactions preference
- [x] User settings page
- [x] Profile management

### Transaction Management
- [x] Manual transaction add/edit/delete
- [x] Transaction listing and filtering
- [x] Category assignment
- [x] Envelope assignment
- [x] Transaction notes
- [x] Date-based organization

### Auto-Detection System
- [x] CSV file import
- [x] OFX/QFX file import
- [x] Merchant normalization (rule-based)
- [x] Category detection (keyword matching)
- [x] Confidence scoring (High/Medium/Low)
- [x] Online sale detection
- [x] Detected transactions review UI
- [x] Accept/reject workflow

### Envelopes & Budgeting
- [x] Create/manage envelopes
- [x] Budget allocation
- [x] Spending tracking per envelope
- [x] Pooled/shared envelope support
- [x] Fund transfer between envelopes
- [x] Visual progress indicators

### Goals Tracking
- [x] Create savings goals
- [x] Target amount and deadline
- [x] Progress tracking
- [x] Visual progress bars
- [x] Current vs target display

### Forecasting
- [x] Rule-based balance projection
- [x] Daily average spending calculation
- [x] 30/90-day forecast
- [x] Confidence level calculation
- [x] Spending trend analysis
- [x] Top categories and merchants
- [x] Monthly spending trends
- [x] Budget breach detection and explanation

### Online Sales & Offers
- [x] Separate online sales page
- [x] E-commerce transaction detection
- [x] Offers management system
- [x] Discount tracking
- [x] Offer expiry dates
- [x] JSON-based offers storage

### Recurring Transactions
- [x] Pattern detection (monthly/weekly)
- [x] Recurring transaction suggestions
- [x] Next expected date calculation
- [x] Average amount tracking
- [x] Occurrence counting

### Reconciliation
- [x] Bank statement upload
- [x] CSV parsing
- [x] Fuzzy matching algorithm
- [x] Date/amount/merchant matching
- [x] Match confidence scoring
- [x] Unmatched transaction reporting
- [x] Match rate calculation

### Data Export & Backup
- [x] CSV export
- [x] Encrypted backup with passphrase
- [x] Per-user data export

### UI/UX
- [x] Responsive design with Tailwind CSS
- [x] Hero background images
- [x] Modern card-based layouts
- [x] Modal dialogs
- [x] Flash messages
- [x] Active navigation highlighting
- [x] Mobile-friendly navigation
- [x] Clean, professional aesthetics

### Testing
- [x] Unit tests for data store
- [x] Unit tests for auto-detection
- [x] Unit tests for forecasting
- [x] pytest configuration

## Acceptance Criteria Testing

### Test Case 1: New User Onboarding
**Steps:**
1. Navigate to http://localhost:8000
2. Click "Sign Up"
3. Enter username, email, password, confirm password
4. Check "Enable auto-detect transactions"
5. Submit form

**Expected Result:**
- User account created
- Automatically logged in
- Redirected to dashboard
- Empty state (no transactions)
- User file created in `data/users/<user_id>.txt`

### Test Case 2: Manual Transaction Entry
**Steps:**
1. Log in as existing user
2. Click "Add Transaction" on dashboard
3. Enter: Merchant="Coffee Shop", Amount=-5.50, Date=today, Category="Food & Dining"
4. Submit

**Expected Result:**
- Transaction appears in recent transactions list
- Transaction saved to database
- Transaction appended to user's .txt file
- Balance updated on dashboard

### Test Case 3: CSV Import & Auto-Detection
**Steps:**
1. Create CSV file with columns: date, amount, merchant
2. Add sample rows (e.g., "2024-01-15,-25.00,AMZN MKTP US")
3. Go to Transactions page
4. Click "Import CSV/OFX"
5. Upload file

**Expected Result:**
- Redirected to Detected Transactions page
- Transactions shown with confidence badges
- Merchant normalized (AMZN MKTP US → Amazon)
- Category auto-assigned
- Accept button available for each transaction

### Test Case 4: Accept Detected Transaction
**Steps:**
1. From detected transactions page
2. Click "Accept" on a transaction

**Expected Result:**
- Transaction moved to regular transactions
- Appears in Transactions page
- Saved to database and .txt file
- Removed from detected list

### Test Case 5: Envelope Creation & Tracking
**Steps:**
1. Go to Envelopes page
2. Click "Create Envelope"
3. Enter: Name="Groceries", Allocated=500
4. Submit
5. Add transaction with envelope assigned

**Expected Result:**
- Envelope created and displayed
- Shows allocated amount
- Spent amount updates when transaction added
- Progress bar reflects spending
- Remaining amount calculated correctly

### Test Case 6: Forecast Projection
**Steps:**
1. Add 20+ transactions over past month
2. Go to Forecast page

**Expected Result:**
- Current balance displayed
- 90-day projection shown
- Confidence level displayed (Medium or High with enough data)
- Daily projection chart visible
- Top categories and merchants listed
- Monthly trend chart displayed

### Test Case 7: Recurring Detection
**Steps:**
1. Add 3+ transactions to same merchant at ~30-day intervals
2. Go to Recurring page

**Expected Result:**
- Recurring pattern detected
- Pattern type shown (Monthly)
- Average amount calculated
- Next expected date displayed
- Occurrence count shown

### Test Case 8: Reconciliation
**Steps:**
1. Create bank statement CSV
2. Go to Reconcile page
3. Upload statement

**Expected Result:**
- Reconciliation results page shown
- Matched transactions listed with confidence
- Unmatched statement transactions listed
- Unmatched user transactions listed
- Match rate percentage displayed

## Future Enhancements (Not Implemented)

### Phase 2 Features
- [ ] Multi-currency support
- [ ] Receipt image upload and storage
- [ ] Transaction search and advanced filtering
- [ ] Budget alerts and notifications
- [ ] Email notifications for recurring payments
- [ ] Shared household accounts
- [ ] Mobile app (React Native)
- [ ] API endpoints for third-party integrations

### Phase 3 Features
- [ ] Investment tracking
- [ ] Net worth calculation
- [ ] Bill reminders
- [ ] Subscription management
- [ ] Tax category tagging
- [ ] Report generation (PDF)
- [ ] Data import from Mint, YNAB, etc.
- [ ] Plaid integration for automatic bank sync

### Performance Optimizations
- [ ] Database indexing optimization
- [ ] Caching layer (Redis)
- [ ] Lazy loading for large transaction lists
- [ ] Background job processing (Celery)
- [ ] CDN for static assets

### Security Enhancements
- [ ] Two-factor authentication (2FA)
- [ ] OAuth login (Google, GitHub)
- [ ] Rate limiting
- [ ] CSRF protection enhancements
- [ ] Security headers (CSP, HSTS)
- [ ] Audit logging

## Known Issues

1. **OFX Import**: Requires `ofxparse` library which may have compatibility issues with some bank formats
2. **File Locking**: Simple file locking may not handle high concurrency well
3. **Date Parsing**: CSV date format detection may fail for unusual formats
4. **Mobile Menu**: Hamburger menu not yet implemented (navigation wraps on mobile)

## Development Guidelines

### Adding New Features
1. Create feature branch
2. Write tests first (TDD approach)
3. Implement feature
4. Update documentation
5. Run full test suite
6. Submit for review

### Code Style
- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write docstrings for all functions
- Keep functions small and focused
- Use meaningful variable names

### Testing Requirements
- Minimum 80% code coverage
- All new features must have tests
- Run `pytest` before committing
- Test edge cases and error conditions

## Link Tracking Feature - QA & Security Review

### QA Tasks
- [ ] Run unit tests: `pytest tests/test_link_tracking.py`
- [ ] Test all 15 end-to-end scenarios from TEST_PLAN.md
- [ ] Verify cart icon updates in real-time
- [ ] Test accept/reject workflow
- [ ] Verify transaction persistence to .txt files
- [ ] Test with multiple users simultaneously
- [ ] Test anonymous (logged-out) clicks
- [ ] Verify database integrity after operations

### Security Review Tasks
- [ ] Review safe redirect whitelist implementation
- [ ] Test open redirect prevention
- [ ] Test XSS prevention in merchant names
- [ ] Test SQL injection attempts
- [ ] Review CSRF protection on POST endpoints
- [ ] Verify user data isolation
- [ ] Check file permission security
- [ ] Review session handling
- [ ] Test URL parameter validation
- [ ] Audit database queries for parameterization

### Performance Tasks
- [ ] Test with 100+ items in cart
- [ ] Test concurrent click recording
- [ ] Measure page load times
- [ ] Check database query optimization
- [ ] Test session storage limits

### Documentation Tasks
- [ ] Update USER_GUIDE.md with link tracking instructions
- [ ] Document safe domain whitelist management
- [ ] Add troubleshooting section
- [ ] Create admin guide for tracking analytics

## Priority Backlog

### High Priority
1. Link tracking feature QA and security review
2. Mobile hamburger menu implementation
3. Transaction edit functionality
4. Envelope deletion with transaction reassignment
5. Goal progress updates

### Medium Priority
1. Advanced search and filtering
2. Bulk transaction operations
3. Custom categories
4. Report generation
5. Link tracking analytics dashboard

### Low Priority
1. Keyboard shortcuts
2. Transaction templates
3. Budget templates
4. Link tracking A/B testing

## Contributing

When working on tasks:
1. Update this file with progress
2. Move completed items to "Completed Features"
3. Add new issues to "Known Issues"
4. Document acceptance criteria for new features
