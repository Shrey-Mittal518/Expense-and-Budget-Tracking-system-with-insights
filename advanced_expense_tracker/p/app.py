"""
Main Flask application for AdvancedExpenseTrackerPro
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from datetime import datetime
import json

from models.user import User
from services.data_store import DataStore
from services.auto_detect import AutoDetector
from services.forecaster import Forecaster
from services.offers import OffersManager
from services.reconciliation import Reconciler
from services.link_tracker import LinkTracker

load_dotenv()

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    app.config['DATABASE_PATH'] = os.getenv('DATABASE_PATH', 'data/expense_tracker.db')
    app.config['USER_DATA_PATH'] = os.getenv('USER_DATA_PATH', 'data/users')
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    # Initialize data store
    os.makedirs('data', exist_ok=True)
    os.makedirs(app.config['USER_DATA_PATH'], exist_ok=True)
    
    data_store = DataStore(app.config['DATABASE_PATH'], app.config['USER_DATA_PATH'])
    data_store.init_db()
    
    # Initialize link tracker
    link_tracker = LinkTracker(app.config['DATABASE_PATH'])
    
    @login_manager.user_loader
    def load_user(user_id):
        return data_store.get_user_by_id(int(user_id))
    
    # Routes
    @app.route('/')
    @login_required
    def index():
        """Dashboard home page"""
        transactions = data_store.get_transactions(current_user.id, limit=10)
        envelopes = data_store.get_envelopes(current_user.id)
        goals = data_store.get_goals(current_user.id)
        
        # Calculate balance (income - expenses)
        all_transactions = data_store.get_transactions(current_user.id)
        income = sum(t['amount'] for t in all_transactions if t['amount'] > 0)
        expenses = sum(abs(t['amount']) for t in all_transactions if t['amount'] < 0)
        balance = income - expenses
        
        # Check for overspending envelopes
        overspent_envelopes = [env for env in envelopes if env['spent'] > env['allocated']]
        
        # Get forecast
        forecaster = Forecaster(data_store)
        forecast_data = forecaster.forecast_balance(current_user.id, days=30)
        
        return render_template('index.html', 
                             balance=balance,
                             income=income,
                             expenses=expenses,
                             transactions=transactions,
                             envelopes=envelopes,
                             goals=goals,
                             forecast=forecast_data,
                             overspent_envelopes=overspent_envelopes)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login"""
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = data_store.authenticate_user(email, password)
            if user:
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password', 'error')
        
        return render_template('login.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        """User registration"""
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            auto_detect = request.form.get('auto_detect') == 'on'
            
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('signup.html')
            
            user = data_store.create_user(username, email, password, auto_detect)
            if user:
                login_user(user)
                flash('Account created successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Email already exists', 'error')
        
        return render_template('signup.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        """User logout"""
        logout_user()
        return redirect(url_for('login'))
    
    @app.route('/transactions')
    @login_required
    def transactions():
        """Transactions page"""
        all_transactions = data_store.get_transactions(current_user.id)
        categories = data_store.get_categories()
        envelopes = data_store.get_envelopes(current_user.id)
        return render_template('transactions.html', 
                             transactions=all_transactions,
                             categories=categories,
                             envelopes=envelopes)
    
    @app.route('/transactions/add', methods=['POST'])
    @login_required
    def add_transaction():
        """Add new transaction"""
        data = request.form
        transaction_id = data_store.add_transaction(
            user_id=current_user.id,
            amount=float(data.get('amount')),
            merchant=data.get('merchant'),
            category=data.get('category'),
            date=data.get('date'),
            envelope_id=data.get('envelope_id') or None,
            notes=data.get('notes', '')
        )
        flash('Transaction added successfully', 'success')
        return redirect(url_for('transactions'))
    
    @app.route('/transactions/delete/<int:transaction_id>', methods=['POST'])
    @login_required
    def delete_transaction(transaction_id):
        """Delete transaction"""
        data_store.delete_transaction(transaction_id, current_user.id)
        flash('Transaction deleted', 'success')
        return redirect(url_for('transactions'))
    
    @app.route('/transactions/import', methods=['POST'])
    @login_required
    def import_transactions():
        """Import transactions from CSV/OFX"""
        if 'file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(url_for('transactions'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('transactions'))
        
        detector = AutoDetector(data_store)
        detected = detector.import_file(file, current_user.id)
        
        # Store detected transactions in session for review
        data_store.store_detected_transactions(current_user.id, detected)
        
        flash(f'{len(detected)} transactions detected', 'success')
        return redirect(url_for('detected_transactions'))
    
    @app.route('/transactions/detected')
    @login_required
    def detected_transactions():
        """View detected transactions"""
        detected = data_store.get_detected_transactions(current_user.id)
        categories = data_store.get_categories()
        envelopes = data_store.get_envelopes(current_user.id)
        return render_template('detected.html', 
                             detected=detected,
                             categories=categories,
                             envelopes=envelopes)
    
    @app.route('/transactions/detected/accept/<int:detected_id>', methods=['POST'])
    @login_required
    def accept_detected(detected_id):
        """Accept a detected transaction"""
        data_store.accept_detected_transaction(detected_id, current_user.id)
        flash('Transaction accepted', 'success')
        return redirect(url_for('detected_transactions'))
    
    @app.route('/transactions/detected/reject/<int:detected_id>', methods=['POST'])
    @login_required
    def reject_detected(detected_id):
        """Reject a detected transaction"""
        data_store.reject_detected_transaction(detected_id, current_user.id)
        return redirect(url_for('detected_transactions'))
    
    @app.route('/envelopes')
    @login_required
    def envelopes():
        """Envelopes page"""
        user_envelopes = data_store.get_envelopes(current_user.id)
        
        # Calculate available balance
        all_transactions = data_store.get_transactions(current_user.id)
        income = sum(t['amount'] for t in all_transactions if t['amount'] > 0)
        expenses = sum(abs(t['amount']) for t in all_transactions if t['amount'] < 0)
        balance = income - expenses
        
        return render_template('envelopes.html', envelopes=user_envelopes, balance=balance)
    
    @app.route('/envelopes/add', methods=['POST'])
    @login_required
    def add_envelope():
        """Create new envelope"""
        name = request.form.get('name')
        allocated = float(request.form.get('allocated', 0))
        is_pooled = request.form.get('is_pooled') == 'on'
        
        data_store.create_envelope(current_user.id, name, allocated, is_pooled)
        flash('Envelope created', 'success')
        return redirect(url_for('envelopes'))
    
    @app.route('/envelopes/allocate', methods=['POST'])
    @login_required
    def allocate_from_balance():
        """Allocate funds from balance to envelope"""
        to_id = int(request.form.get('to_envelope'))
        amount = float(request.form.get('amount'))
        
        # Check if user has sufficient balance
        all_transactions = data_store.get_transactions(current_user.id)
        income = sum(t['amount'] for t in all_transactions if t['amount'] > 0)
        expenses = sum(abs(t['amount']) for t in all_transactions if t['amount'] < 0)
        balance = income - expenses
        
        if amount > balance:
            flash(f'Insufficient balance. Available: ₹{balance:.2f}', 'error')
            return redirect(url_for('envelopes'))
        
        # Allocate funds to envelope
        data_store.allocate_to_envelope(to_id, amount, current_user.id)
        flash(f'₹{amount:.2f} allocated successfully', 'success')
        return redirect(url_for('envelopes'))
    
    @app.route('/envelopes/transfer', methods=['POST'])
    @login_required
    def transfer_envelope():
        """Transfer funds between envelopes"""
        from_id = int(request.form.get('from_envelope'))
        to_id = int(request.form.get('to_envelope'))
        amount = float(request.form.get('amount'))
        
        if from_id == to_id:
            flash('Cannot transfer to the same envelope', 'error')
            return redirect(url_for('envelopes'))
        
        data_store.transfer_envelope_funds(from_id, to_id, amount, current_user.id)
        flash('Transfer completed', 'success')
        return redirect(url_for('envelopes'))
    
    @app.route('/goals')
    @login_required
    def goals():
        """Goals tracking page"""
        user_goals = data_store.get_goals(current_user.id)
        return render_template('goals.html', goals=user_goals)
    
    @app.route('/goals/add', methods=['POST'])
    @login_required
    def add_goal():
        """Create new goal"""
        name = request.form.get('name')
        target = float(request.form.get('target'))
        current = float(request.form.get('current', 0))
        deadline = request.form.get('deadline')
        
        data_store.create_goal(current_user.id, name, target, current, deadline)
        flash('Goal created', 'success')
        return redirect(url_for('goals'))
    
    @app.route('/goals/delete/<int:goal_id>', methods=['POST'])
    @login_required
    def delete_goal(goal_id):
        """Delete a goal"""
        data_store.delete_goal(goal_id, current_user.id)
        flash('Goal deleted successfully', 'success')
        return redirect(url_for('goals'))
    
    @app.route('/goals/contribute', methods=['POST'])
    @login_required
    def contribute_to_goal():
        """Contribute funds to a goal"""
        goal_id = int(request.form.get('goal_id'))
        amount = float(request.form.get('amount'))
        
        if amount <= 0:
            flash('Contribution amount must be positive', 'error')
            return redirect(url_for('goals'))
        
        # Check if user has sufficient balance
        all_transactions = data_store.get_transactions(current_user.id)
        income = sum(t['amount'] for t in all_transactions if t['amount'] > 0)
        expenses = sum(abs(t['amount']) for t in all_transactions if t['amount'] < 0)
        balance = income - expenses
        
        if amount > balance:
            flash(f'Insufficient balance. Available: ₹{balance:.2f}', 'error')
            return redirect(url_for('goals'))
        
        # Get goal details before contribution
        goals = data_store.get_goals(current_user.id)
        goal = next((g for g in goals if g['id'] == goal_id), None)
        
        if not goal:
            flash('Goal not found', 'error')
            return redirect(url_for('goals'))
        
        # Contribute to goal
        data_store.contribute_to_goal(goal_id, amount, current_user.id)
        
        # Check if goal is now completed
        new_current = goal['current'] + amount
        if new_current >= goal['target'] and goal['current'] < goal['target']:
            # Goal just completed!
            flash(f'🎉 Congratulations! You\'ve completed your "{goal["name"]}" goal! 🎉', 'goal_completed')
        else:
            flash(f'₹{amount:.2f} contributed to goal successfully', 'success')
        
        return redirect(url_for('goals'))
    
    @app.route('/forecast')
    @login_required
    def forecast():
        """Forecast page"""
        forecaster = Forecaster(data_store)
        forecast_data = forecaster.forecast_balance(current_user.id, days=90)
        spending_trends = forecaster.analyze_spending_trends(current_user.id)
        
        return render_template('forecast.html', 
                             forecast=forecast_data,
                             trends=spending_trends)
    
    @app.route('/online-sales')
    @login_required
    def online_sales():
        """Online sales transactions page"""
        sales = data_store.get_online_sales(current_user.id)
        return render_template('online_sales.html', sales=sales)
    
    @app.route('/offers')
    @login_required
    def offers():
        """Offers management page"""
        offers_mgr = OffersManager()
        all_offers = offers_mgr.get_offers(current_user.id)
        live_offers_data = offers_mgr.get_live_offers()
        
        # Create tracking links for live offers
        live_offers_with_tracking = {}
        for site_name, site_info in live_offers_data.items():
            offers_with_links = []
            for offer in site_info['offers']:
                # Estimate amount based on discount (placeholder logic)
                estimated_amount = 1000  # Default estimate
                
                tracking_id, tracking_url = link_tracker.create_tracking_link(
                    user_id=current_user.id,
                    merchant=site_name,
                    title=offer['title'],
                    amount=estimated_amount,
                    target_url=site_info['url']
                )
                
                offer_with_link = offer.copy()
                offer_with_link['tracking_url'] = tracking_url
                offer_with_link['tracking_id'] = tracking_id
                offers_with_links.append(offer_with_link)
            
            site_with_tracking = site_info.copy()
            site_with_tracking['offers'] = offers_with_links
            live_offers_with_tracking[site_name] = site_with_tracking
        
        return render_template('offers.html', 
                             offers=all_offers, 
                             live_offers=live_offers_with_tracking)
    
    @app.route('/offers/add', methods=['POST'])
    @login_required
    def add_offer():
        """Add new offer"""
        offers_mgr = OffersManager()
        offers_mgr.add_offer(
            user_id=current_user.id,
            merchant=request.form.get('merchant'),
            discount=float(request.form.get('discount')),
            description=request.form.get('description'),
            expiry=request.form.get('expiry')
        )
        flash('Offer added', 'success')
        return redirect(url_for('offers'))
    
    @app.route('/recurring')
    @login_required
    def recurring():
        """Recurring transactions page"""
        detector = AutoDetector(data_store)
        recurring_items = detector.detect_recurring(current_user.id)
        return render_template('recurring.html', recurring=recurring_items)
    
    @app.route('/reconcile')
    @login_required
    def reconcile():
        """Reconciliation page"""
        return render_template('reconcile.html')
    
    @app.route('/reconcile/upload', methods=['POST'])
    @login_required
    def reconcile_upload():
        """Upload statement for reconciliation"""
        if 'file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(url_for('reconcile'))
        
        file = request.files['file']
        reconciler = Reconciler(data_store)
        results = reconciler.reconcile_statement(file, current_user.id)
        
        return render_template('reconcile_results.html', results=results)
    
    @app.route('/settings')
    @login_required
    def settings():
        """Settings page"""
        return render_template('settings.html', user=current_user)
    
    @app.route('/settings/update', methods=['POST'])
    @login_required
    def update_settings():
        """Update user settings"""
        username = request.form.get('username')
        auto_detect = request.form.get('auto_detect') == 'on'
        
        data_store.update_user_settings(current_user.id, username, auto_detect)
        flash('Settings updated', 'success')
        return redirect(url_for('settings'))
    
    @app.route('/export/csv')
    @login_required
    def export_csv():
        """Export transactions to CSV"""
        csv_path = data_store.export_to_csv(current_user.id)
        return send_file(csv_path, as_attachment=True)
    
    @app.route('/export/backup', methods=['POST'])
    @login_required
    def export_backup():
        """Create encrypted backup"""
        passphrase = request.form.get('passphrase')
        backup_path = data_store.create_encrypted_backup(current_user.id, passphrase)
        return send_file(backup_path, as_attachment=True)
    
    # Link Tracking Routes
    @app.route('/track/<tracking_id>')
    def track(tracking_id):
        """Track link click and create transaction immediately"""
        # Get tracking metadata
        meta = link_tracker.get_tracked_item(tracking_id)
        if not meta:
            flash('Invalid tracking link', 'error')
            return redirect(url_for('index'))
        
        # Must be logged in to create transactions
        if not current_user.is_authenticated:
            flash('Please log in to track purchases', 'error')
            return redirect(url_for('login'))
        
        # Record click
        link_tracker.record_click(
            tracking_id,
            current_user.id,
            request.remote_addr,
            request.user_agent.string,
            request.referrer,
            datetime.now(),
            ''
        )
        
        # Create transaction immediately (not detected, but actual transaction)
        amount = meta['amount'] if meta['amount'] else 1000  # Default if no amount
        transaction_id = data_store.add_transaction(
            user_id=current_user.id,
            amount=-abs(amount),  # Negative for expense
            merchant=meta['merchant'],
            category='Shopping',
            date=datetime.now().strftime('%Y-%m-%d'),
            notes=f"From {meta['title']} | tracking_id={tracking_id}"
        )
        
        # Mark click as accepted
        link_tracker.mark_click_accepted(tracking_id, current_user.id)
        
        flash(f'Purchase tracked! ₹{abs(amount):.2f} added to {meta["merchant"]}', 'success')
        
        # Redirect behavior
        redirect_enabled = request.args.get('redirect', '1') == '1'
        
        if redirect_enabled and link_tracker.is_safe_redirect(meta['target_url']):
            return redirect(meta['target_url'])
        else:
            return redirect(url_for('transactions'))
    
    @app.route('/cart')
    @login_required
    def cart():
        """View shopping cart and click history"""
        recent_clicks = link_tracker.get_user_clicks(current_user.id, limit=20)
        click_stats = link_tracker.get_click_stats(current_user.id)
        
        # Get recent transactions from tracking
        recent_tracked_transactions = []
        for click in recent_clicks:
            if click['accepted_flag'] == 1:
                # Find the corresponding transaction
                transactions = data_store.get_transactions(current_user.id)
                for t in transactions:
                    if click['tracking_id'] in str(t.get('notes', '')):
                        recent_tracked_transactions.append({
                            'transaction': t,
                            'click': click
                        })
                        break
        
        return render_template('cart.html', 
                             recent_clicks=recent_clicks,
                             tracked_transactions=recent_tracked_transactions,
                             stats=click_stats)
    

    
    return app

    # Link Tracking Route - Simplified
    @app.route('/track/<tracking_id>')
    def track_purchase(tracking_id):
        """Track link click and create transaction immediately"""
        # Get tracking metadata
        meta = link_tracker.get_tracked_item(tracking_id)
        if not meta:
            flash('Invalid tracking link', 'error')
            return redirect(url_for('index'))
        
        # Must be logged in to create transactions
        if not current_user.is_authenticated:
            flash('Please log in to track purchases', 'error')
            return redirect(url_for('login'))
        
        # Record click
        link_tracker.record_click(
            tracking_id,
            current_user.id,
            request.remote_addr,
            request.user_agent.string,
            request.referrer,
            datetime.now(),
            ''
        )
        
        # Create transaction immediately (not detected, but actual transaction)
        amount = meta['amount'] if meta['amount'] else 1000  # Default if no amount
        transaction_id = data_store.add_transaction(
            user_id=current_user.id,
            amount=-abs(amount),  # Negative for expense
            merchant=meta['merchant'],
            category='Shopping',
            date=datetime.now().strftime('%Y-%m-%d'),
            notes=f"From {meta['title']} | tracking_id={tracking_id}"
        )
        
        # Mark click as accepted
        link_tracker.mark_click_accepted(tracking_id, current_user.id)
        
        flash(f'Purchase tracked! ₹{abs(amount):.2f} added to {meta["merchant"]}', 'success')
        
        # Redirect to transactions page to show the new transaction
        return redirect(url_for('transactions'))
    
    @app.route('/cart')
    @login_required
    def cart():
        """View purchase history and click statistics"""
        recent_clicks = link_tracker.get_user_clicks(current_user.id, limit=20)
        click_stats = link_tracker.get_click_stats(current_user.id)
        
        # Get recent transactions from tracking
        recent_tracked_transactions = []
        for click in recent_clicks:
            if click['accepted_flag'] == 1:
                # Find the corresponding transaction
                transactions = data_store.get_transactions(current_user.id)
                for t in transactions:
                    if click['tracking_id'] in str(t.get('notes', '')):
                        recent_tracked_transactions.append({
                            'transaction': t,
                            'click': click
                        })
                        break
        
        return render_template('cart.html', 
                             recent_clicks=recent_clicks,
                             tracked_transactions=recent_tracked_transactions,
                             stats=click_stats)
