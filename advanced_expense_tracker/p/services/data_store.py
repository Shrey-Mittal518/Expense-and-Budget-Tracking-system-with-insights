"""
Data storage service using SQLite and per-user text files
"""
import sqlite3
import bcrypt
import os
import csv
from datetime import datetime
from threading import Lock
from cryptography.fernet import Fernet
import base64
import hashlib

from models.user import User
from models.transaction import Transaction
from models.envelope import Envelope

class DataStore:
    """Manages all data persistence"""
    
    def __init__(self, db_path, user_data_path):
        self.db_path = db_path
        self.user_data_path = user_data_path
        self.file_locks = {}
        self.lock = Lock()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                auto_detect_enabled INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                merchant TEXT NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                envelope_id INTEGER,
                notes TEXT,
                is_online_sale INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Envelopes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS envelopes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                allocated REAL NOT NULL,
                spent REAL DEFAULT 0,
                is_pooled INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                target REAL NOT NULL,
                current REAL DEFAULT 0,
                deadline TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Detected transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detected_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                merchant TEXT NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                confidence TEXT NOT NULL,
                is_online_sale INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username, email, password, auto_detect=False):
        """Create new user with hashed password"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, auto_detect_enabled)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, 1 if auto_detect else 0))
            conn.commit()
            user_id = cursor.lastrowid
            
            # Create user text file
            user_file = self._get_user_file_path(user_id)
            with open(user_file, 'w') as f:
                f.write(f"# Transaction log for user {user_id}\n")
            
            conn.close()
            return User(user_id, username, email, auto_detect)
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def authenticate_user(self, email, password):
        """Authenticate user credentials"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row and bcrypt.checkpw(password.encode('utf-8'), row['password_hash']):
            return User(row['id'], row['username'], row['email'], row['auto_detect_enabled'])
        return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(row['id'], row['username'], row['email'], row['auto_detect_enabled'])
        return None
    
    def _get_user_file_path(self, user_id):
        """Get path to user's transaction log file"""
        # Sanitize user_id to prevent path traversal
        safe_user_id = str(int(user_id))
        return os.path.join(self.user_data_path, f'{safe_user_id}.txt')
    
    def _append_to_user_file(self, user_id, transaction_data):
        """Append transaction to user's text file"""
        user_file = self._get_user_file_path(user_id)
        
        # Simple file locking
        with self.lock:
            with open(user_file, 'a') as f:
                line = f"{transaction_data['date']} | {transaction_data['amount']} | {transaction_data['merchant']} | {transaction_data['category']} | {transaction_data.get('notes', '')}\n"
                f.write(line)
    
    def add_transaction(self, user_id, amount, merchant, category, date, envelope_id=None, notes=''):
        """Add new transaction"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Detect if online sale
        is_online_sale = self._is_online_merchant(merchant)
        
        cursor.execute('''
            INSERT INTO transactions (user_id, amount, merchant, category, date, envelope_id, notes, is_online_sale)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, amount, merchant, category, date, envelope_id, notes, 1 if is_online_sale else 0))
        
        transaction_id = cursor.lastrowid
        
        # Update envelope if specified
        if envelope_id:
            cursor.execute('UPDATE envelopes SET spent = spent + ? WHERE id = ?', (abs(amount), envelope_id))
        
        conn.commit()
        conn.close()
        
        # Append to user file
        self._append_to_user_file(user_id, {
            'date': date,
            'amount': amount,
            'merchant': merchant,
            'category': category,
            'notes': notes
        })
        
        return transaction_id
    
    def _is_online_merchant(self, merchant):
        """Detect if merchant is online"""
        online_keywords = ['amazon', 'ebay', 'etsy', 'shopify', 'paypal', 'stripe', 'online', 'web']
        merchant_lower = merchant.lower()
        return any(keyword in merchant_lower for keyword in online_keywords)
    
    def get_transactions(self, user_id, limit=None):
        """Get user transactions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC'
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def delete_transaction(self, transaction_id, user_id):
        """Delete transaction"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM transactions WHERE id = ? AND user_id = ?', (transaction_id, user_id))
        conn.commit()
        conn.close()
    
    def create_envelope(self, user_id, name, allocated, is_pooled=False):
        """Create new envelope"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO envelopes (user_id, name, allocated, is_pooled)
            VALUES (?, ?, ?, ?)
        ''', (user_id, name, allocated, 1 if is_pooled else 0))
        
        conn.commit()
        conn.close()
    
    def get_envelopes(self, user_id):
        """Get user envelopes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM envelopes WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def allocate_to_envelope(self, envelope_id, amount, user_id):
        """Allocate funds from balance to envelope"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE envelopes SET allocated = allocated + ? WHERE id = ? AND user_id = ?', 
                      (amount, envelope_id, user_id))
        
        conn.commit()
        conn.close()
    
    def transfer_envelope_funds(self, from_id, to_id, amount, user_id):
        """Transfer funds between envelopes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if source envelope has sufficient funds
        cursor.execute('SELECT allocated FROM envelopes WHERE id = ? AND user_id = ?', (from_id, user_id))
        row = cursor.fetchone()
        
        if row and row['allocated'] >= amount:
            cursor.execute('UPDATE envelopes SET allocated = allocated - ? WHERE id = ? AND user_id = ?', 
                          (amount, from_id, user_id))
            cursor.execute('UPDATE envelopes SET allocated = allocated + ? WHERE id = ? AND user_id = ?', 
                          (amount, to_id, user_id))
            conn.commit()
        
        conn.close()
    
    def create_goal(self, user_id, name, target, current, deadline):
        """Create savings goal"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO goals (user_id, name, target, current, deadline)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, name, target, current, deadline))
        
        conn.commit()
        conn.close()
    
    def get_goals(self, user_id):
        """Get user goals"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM goals WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def contribute_to_goal(self, goal_id, amount, user_id):
        """Contribute funds to a goal"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Update goal current amount
        cursor.execute('''
            UPDATE goals 
            SET current = current + ?
            WHERE id = ? AND user_id = ?
        ''', (amount, goal_id, user_id))
        
        conn.commit()
        conn.close()
    
    def delete_goal(self, goal_id, user_id):
        """Delete a goal"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM goals 
            WHERE id = ? AND user_id = ?
        ''', (goal_id, user_id))
        
        conn.commit()
        conn.close()
    
    def get_online_sales(self, user_id):
        """Get online sale transactions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM transactions WHERE user_id = ? AND is_online_sale = 1 ORDER BY date DESC', 
                      (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def store_detected_transactions(self, user_id, detected):
        """Store detected transactions for review"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for item in detected:
            cursor.execute('''
                INSERT INTO detected_transactions (user_id, amount, merchant, category, date, confidence, is_online_sale)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, item['amount'], item['merchant'], item['category'], 
                  item['date'], item['confidence'], 1 if item.get('is_online_sale') else 0))
        
        conn.commit()
        conn.close()
    
    def get_detected_transactions(self, user_id):
        """Get pending detected transactions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM detected_transactions WHERE user_id = ? ORDER BY date DESC', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def accept_detected_transaction(self, detected_id, user_id, tracking_id=None):
        """Accept and convert detected transaction to regular transaction"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM detected_transactions WHERE id = ? AND user_id = ?', 
                      (detected_id, user_id))
        row = cursor.fetchone()
        
        if row:
            notes = f"Auto-detected ({row['confidence']} confidence)"
            if tracking_id:
                notes += f" | tracking_id={tracking_id}"
            
            self.add_transaction(user_id, row['amount'], row['merchant'], row['category'], 
                               row['date'], notes=notes)
            cursor.execute('DELETE FROM detected_transactions WHERE id = ?', (detected_id,))
            conn.commit()
        
        conn.close()
    
    def create_detected_from_link(self, user_id, merchant, amount, tracking_id, confidence='Medium'):
        """Create a detected transaction from a tracking link"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Use negative amount for purchases
        if amount and amount > 0:
            amount = -abs(amount)
        
        cursor.execute('''
            INSERT INTO detected_transactions 
            (user_id, amount, merchant, category, date, confidence, is_online_sale)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, amount, merchant, 'Shopping', datetime.now().strftime('%Y-%m-%d'), 
              confidence, 1))
        
        detected_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return detected_id
    
    def reject_detected_transaction(self, detected_id, user_id):
        """Reject detected transaction"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM detected_transactions WHERE id = ? AND user_id = ?', 
                      (detected_id, user_id))
        conn.commit()
        conn.close()
    
    def get_categories(self):
        """Get available categories"""
        return ['Food & Dining', 'Shopping', 'Transportation', 'Bills & Utilities', 
                'Entertainment', 'Healthcare', 'Travel', 'Income', 'Other']
    
    def update_user_settings(self, user_id, username, auto_detect):
        """Update user settings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET username = ?, auto_detect_enabled = ? WHERE id = ?
        ''', (username, 1 if auto_detect else 0, user_id))
        
        conn.commit()
        conn.close()
    
    def export_to_csv(self, user_id):
        """Export transactions to CSV"""
        transactions = self.get_transactions(user_id)
        
        export_path = os.path.join(self.user_data_path, f'export_{user_id}_{datetime.now().strftime("%Y%m%d")}.csv')
        
        with open(export_path, 'w', newline='') as f:
            if transactions:
                writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
                writer.writeheader()
                writer.writerows(transactions)
        
        return export_path
    
    def create_encrypted_backup(self, user_id, passphrase):
        """Create encrypted backup of user data"""
        # Generate key from passphrase
        key = base64.urlsafe_b64encode(hashlib.sha256(passphrase.encode()).digest())
        fernet = Fernet(key)
        
        # Read user file
        user_file = self._get_user_file_path(user_id)
        with open(user_file, 'rb') as f:
            data = f.read()
        
        # Encrypt
        encrypted = fernet.encrypt(data)
        
        # Save backup
        backup_path = os.path.join(self.user_data_path, f'backup_{user_id}_{datetime.now().strftime("%Y%m%d")}.enc')
        with open(backup_path, 'wb') as f:
            f.write(encrypted)
        
        return backup_path
