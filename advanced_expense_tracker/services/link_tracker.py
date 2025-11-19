"""
Link-based purchase tracking service
Tracks clicks on shopping/offer links and creates detected transactions
"""
import sqlite3
import uuid
from datetime import datetime
from urllib.parse import urlparse

class LinkTracker:
    """Manages tracking links and click recording"""
    
    # Whitelist of safe redirect domains
    SAFE_DOMAINS = [
        'amazon.in', 'amazon.com',
        'flipkart.com',
        'myntra.com',
        'swiggy.com',
        'zomato.com',
        'paytm.com',
        'snapdeal.com',
        'ajio.com',
        'nykaa.com'
    ]
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_tables()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_tables(self):
        """Initialize tracking tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Link tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS link_tracking (
                tracking_id TEXT PRIMARY KEY,
                merchant TEXT NOT NULL,
                title TEXT NOT NULL,
                amount REAL,
                target_url TEXT NOT NULL,
                offer_id INTEGER,
                created_by_user INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by_user) REFERENCES users(id)
            )
        ''')
        
        # Link clicks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS link_clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_id TEXT NOT NULL,
                user_id INTEGER,
                ip TEXT,
                user_agent TEXT,
                referer TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                accepted_flag INTEGER DEFAULT 0,
                extra_meta TEXT,
                FOREIGN KEY (tracking_id) REFERENCES link_tracking(tracking_id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_tracking_link(self, user_id, merchant, title, amount, target_url, offer_id=None):
        """
        Create a new tracking link
        Returns: (tracking_id, tracking_url)
        """
        tracking_id = str(uuid.uuid4())
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO link_tracking 
            (tracking_id, merchant, title, amount, target_url, offer_id, created_by_user)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (tracking_id, merchant, title, amount, target_url, offer_id, user_id))
        
        conn.commit()
        conn.close()
        
        tracking_url = f'/track/{tracking_id}'
        return tracking_id, tracking_url
    
    def record_click(self, tracking_id, user_id, ip, user_agent, referer, timestamp, extra_meta=''):
        """Record a click on a tracking link"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO link_clicks 
            (tracking_id, user_id, ip, user_agent, referer, timestamp, extra_meta)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (tracking_id, user_id, ip, user_agent, referer, timestamp, extra_meta))
        
        conn.commit()
        conn.close()
    
    def get_tracked_item(self, tracking_id):
        """Retrieve tracking metadata"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM link_tracking WHERE tracking_id = ?
        ''', (tracking_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def mark_click_accepted(self, tracking_id, user_id):
        """Mark a click as accepted (transaction created)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE link_clicks 
            SET accepted_flag = 1 
            WHERE tracking_id = ? AND user_id = ?
        ''', (tracking_id, user_id))
        
        conn.commit()
        conn.close()
    
    def get_user_clicks(self, user_id, limit=50):
        """Get recent clicks for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT lc.*, lt.merchant, lt.title, lt.amount, lt.target_url
            FROM link_clicks lc
            JOIN link_tracking lt ON lc.tracking_id = lt.tracking_id
            WHERE lc.user_id = ?
            ORDER BY lc.timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def is_safe_redirect(self, url):
        """
        Validate if URL is safe for redirect
        Checks scheme and domain against whitelist
        """
        try:
            parsed = urlparse(url)
            
            # Must be https
            if parsed.scheme != 'https':
                return False
            
            # Check if domain is in whitelist
            hostname = parsed.netloc.lower()
            
            # Remove www. prefix if present
            if hostname.startswith('www.'):
                hostname = hostname[4:]
            
            # Check against whitelist
            for safe_domain in self.SAFE_DOMAINS:
                if hostname == safe_domain or hostname.endswith('.' + safe_domain):
                    return True
            
            return False
        except:
            return False
    
    def calculate_confidence(self, merchant, amount):
        """
        Calculate confidence level for detected transaction
        High: Known merchant + amount present
        Medium: Known merchant OR amount present
        Low: Neither
        """
        known_merchants = [
            'amazon', 'flipkart', 'myntra', 'swiggy', 'zomato', 
            'paytm', 'snapdeal', 'ajio', 'nykaa'
        ]
        
        merchant_lower = merchant.lower()
        is_known = any(km in merchant_lower for km in known_merchants)
        has_amount = amount is not None and amount > 0
        
        if is_known and has_amount:
            return 'High'
        elif is_known or has_amount:
            return 'Medium'
        else:
            return 'Low'
    
    def get_click_stats(self, user_id):
        """Get click statistics for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_clicks,
                SUM(accepted_flag) as accepted_clicks,
                COUNT(DISTINCT tracking_id) as unique_items
            FROM link_clicks
            WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return {'total_clicks': 0, 'accepted_clicks': 0, 'unique_items': 0}
