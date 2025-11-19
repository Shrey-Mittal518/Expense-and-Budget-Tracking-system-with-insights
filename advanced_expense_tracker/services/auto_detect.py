"""
Auto-detection service for transactions using rule-based heuristics
No ML/AI - pure Python logic for merchant normalization and pattern detection
"""
import csv
import re
from datetime import datetime, timedelta
from collections import defaultdict
import io

try:
    from ofxparse import OfxParser
except ImportError:
    OfxParser = None

class AutoDetector:
    """Rule-based transaction detection and normalization"""
    
    # Transaction type keywords (for detecting income vs expense)
    INCOME_KEYWORDS = [
        'credit', 'deposit', 'salary', 'income', 'received', 'receive', 'refund',
        'cashback', 'reward', 'bonus', 'payment received', 'transfer in', 'credited',
        'earn', 'earned', 'revenue', 'sale', 'sold', 'interest', 'dividend'
    ]
    
    EXPENSE_KEYWORDS = [
        'debit', 'withdrawal', 'payment', 'purchase', 'spent', 'spend', 'paid',
        'bill', 'charge', 'fee', 'transfer out', 'debited', 'bought', 'buy',
        'expense', 'cost', 'shopping', 'subscription'
    ]
    
    # Merchant normalization rules
    MERCHANT_PATTERNS = {
        r'AMZN|AMAZON': 'Amazon',
        r'FLIPKART|FKRT': 'Flipkart',
        r'WALMART|WAL-MART|WM SUPERCENTER': 'Walmart',
        r'TARGET': 'Target',
        r'STARBUCKS|SBUX': 'Starbucks',
        r'MCDONALD': 'McDonald\'s',
        r'SHELL|EXXON|CHEVRON|BP\s': 'Gas Station',
        r'UBER|LYFT': 'Rideshare',
        r'NETFLIX': 'Netflix',
        r'SPOTIFY': 'Spotify',
        r'APPLE\.COM|ITUNES': 'Apple',
        r'MYNTRA': 'Myntra',
        r'SWIGGY': 'Swiggy',
        r'ZOMATO': 'Zomato',
        r'PAYTM': 'Paytm',
    }
    
    # Category detection keywords
    CATEGORY_KEYWORDS = {
        'Food & Dining': ['restaurant', 'cafe', 'coffee', 'pizza', 'burger', 'food', 'dining', 
                          'starbucks', 'mcdonald', 'subway', 'chipotle'],
        'Shopping': ['amazon', 'walmart', 'target', 'store', 'shop', 'retail', 'mall'],
        'Transportation': ['uber', 'lyft', 'gas', 'fuel', 'parking', 'transit', 'taxi'],
        'Bills & Utilities': ['electric', 'water', 'internet', 'phone', 'utility', 'bill'],
        'Entertainment': ['netflix', 'spotify', 'movie', 'theater', 'game', 'entertainment'],
        'Healthcare': ['pharmacy', 'doctor', 'hospital', 'medical', 'health', 'cvs', 'walgreens'],
    }
    
    # Online merchant indicators
    ONLINE_INDICATORS = ['amazon', 'ebay', 'etsy', 'paypal', 'stripe', '.com', 'online', 'web']
    
    def __init__(self, data_store):
        self.data_store = data_store
    
    def import_file(self, file, user_id):
        """Import transactions from CSV or OFX file"""
        filename = file.filename.lower()
        
        if filename.endswith('.csv'):
            return self._import_csv(file, user_id)
        elif filename.endswith('.ofx') or filename.endswith('.qfx'):
            return self._import_ofx(file, user_id)
        else:
            return []
    
    def _import_csv(self, file, user_id):
        """Import from CSV with intelligent column detection"""
        detected = []
        
        # Read CSV
        content = file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(content))
        
        for row in reader:
            # Try to detect columns intelligently
            date = self._extract_date(row)
            amount = self._extract_amount(row)
            merchant = self._extract_merchant(row)
            
            if date and amount and merchant:
                # Detect transaction type (income vs expense)
                transaction_type = self._detect_transaction_type(row)
                
                # Adjust amount based on transaction type
                if transaction_type == 'expense' and amount > 0:
                    amount = -abs(amount)
                elif transaction_type == 'income' and amount < 0:
                    amount = abs(amount)
                
                # Normalize merchant
                normalized_merchant = self._normalize_merchant(merchant)
                
                # Detect category
                category = self._detect_category(normalized_merchant, row)
                
                # Calculate confidence
                confidence = self._calculate_confidence(normalized_merchant, category)
                
                # Check if online sale
                is_online = self._is_online_sale(normalized_merchant)
                
                detected.append({
                    'date': date,
                    'amount': amount,
                    'merchant': normalized_merchant,
                    'category': category,
                    'confidence': confidence,
                    'is_online_sale': is_online,
                    'transaction_type': transaction_type
                })
        
        return detected
    
    def _import_ofx(self, file, user_id):
        """Import from OFX/QFX file"""
        if not OfxParser:
            return []
        
        detected = []
        
        try:
            ofx = OfxParser.parse(file)
            
            for account in ofx.accounts:
                for transaction in account.statement.transactions:
                    merchant = transaction.payee or transaction.memo or 'Unknown'
                    normalized_merchant = self._normalize_merchant(merchant)
                    category = self._detect_category(normalized_merchant, {})
                    confidence = self._calculate_confidence(normalized_merchant, category)
                    is_online = self._is_online_sale(normalized_merchant)
                    
                    detected.append({
                        'date': transaction.date.strftime('%Y-%m-%d'),
                        'amount': float(transaction.amount),
                        'merchant': normalized_merchant,
                        'category': category,
                        'confidence': confidence,
                        'is_online_sale': is_online
                    })
        except Exception as e:
            print(f"OFX parse error: {e}")
        
        return detected
    
    def _extract_date(self, row):
        """Extract date from CSV row"""
        date_fields = ['date', 'transaction date', 'posted date', 'trans date']
        
        for field in date_fields:
            for key in row.keys():
                if field in key.lower():
                    try:
                        # Try multiple date formats
                        date_str = row[key]
                        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']:
                            try:
                                return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
                            except:
                                continue
                    except:
                        pass
        
        return datetime.now().strftime('%Y-%m-%d')
    
    def _extract_amount(self, row):
        """Extract amount from CSV row"""
        amount_fields = ['amount', 'debit', 'credit', 'transaction amount']
        
        for field in amount_fields:
            for key in row.keys():
                if field in key.lower():
                    try:
                        amount_str = row[key].replace('$', '').replace(',', '').strip()
                        return float(amount_str)
                    except:
                        pass
        
        return 0.0
    
    def _extract_merchant(self, row):
        """Extract merchant from CSV row"""
        merchant_fields = ['merchant', 'description', 'payee', 'name', 'memo']
        
        for field in merchant_fields:
            for key in row.keys():
                if field in key.lower() and row[key]:
                    return row[key]
        
        return 'Unknown'
    
    def _normalize_merchant(self, merchant):
        """Normalize merchant name using pattern matching"""
        merchant_upper = merchant.upper()
        
        for pattern, normalized in self.MERCHANT_PATTERNS.items():
            if re.search(pattern, merchant_upper):
                return normalized
        
        # Clean up common prefixes/suffixes
        cleaned = re.sub(r'#\d+', '', merchant)  # Remove store numbers
        cleaned = re.sub(r'\d{10,}', '', cleaned)  # Remove long numbers
        cleaned = cleaned.strip()
        
        return cleaned[:50]  # Limit length
    
    def _detect_category(self, merchant, row):
        """Detect category based on merchant and keywords"""
        merchant_lower = merchant.lower()
        
        # Check description field if available
        description = ''
        for key in row.keys():
            if 'description' in key.lower() or 'memo' in key.lower():
                description = row[key].lower()
                break
        
        combined_text = f"{merchant_lower} {description}"
        
        # Score each category
        scores = defaultdict(int)
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in combined_text:
                    scores[category] += 1
        
        if scores:
            return max(scores, key=scores.get)
        
        return 'Other'
    
    def _calculate_confidence(self, merchant, category):
        """Calculate confidence level for detection"""
        confidence_score = 0
        
        # Known merchant patterns increase confidence
        merchant_upper = merchant.upper()
        for pattern in self.MERCHANT_PATTERNS.keys():
            if re.search(pattern, merchant_upper):
                confidence_score += 40
                break
        
        # Category detection adds confidence
        if category != 'Other':
            confidence_score += 30
        
        # Merchant name quality
        if len(merchant) > 3 and not merchant.startswith('Unknown'):
            confidence_score += 30
        
        if confidence_score >= 70:
            return 'High'
        elif confidence_score >= 40:
            return 'Medium'
        else:
            return 'Low'
    
    def _is_online_sale(self, merchant):
        """Detect if transaction is from online merchant"""
        merchant_lower = merchant.lower()
        return any(indicator in merchant_lower for indicator in self.ONLINE_INDICATORS)
    
    def _detect_transaction_type(self, row):
        """Detect if transaction is income or expense from CSV columns"""
        # Check for type/transaction type column
        type_fields = ['type', 'transaction type', 'trans type', 'txn type', 'mode', 'cr/dr']
        
        for field in type_fields:
            for key in row.keys():
                if field in key.lower():
                    value = row[key].lower()
                    
                    # Check for income keywords
                    if any(keyword in value for keyword in self.INCOME_KEYWORDS):
                        return 'income'
                    
                    # Check for expense keywords
                    if any(keyword in value for keyword in self.EXPENSE_KEYWORDS):
                        return 'expense'
        
        # Check description/memo field for keywords
        desc_fields = ['description', 'memo', 'narration', 'details', 'remarks']
        for field in desc_fields:
            for key in row.keys():
                if field in key.lower() and row[key]:
                    value = row[key].lower()
                    
                    # Check for income keywords
                    if any(keyword in value for keyword in self.INCOME_KEYWORDS):
                        return 'income'
                    
                    # Check for expense keywords
                    if any(keyword in value for keyword in self.EXPENSE_KEYWORDS):
                        return 'expense'
        
        # Default to expense if can't determine
        return 'expense'
    
    def detect_recurring(self, user_id):
        """Detect recurring transactions using pattern analysis"""
        transactions = self.data_store.get_transactions(user_id)
        
        # Group by merchant
        merchant_groups = defaultdict(list)
        for t in transactions:
            merchant_groups[t['merchant']].append(t)
        
        recurring = []
        
        for merchant, trans_list in merchant_groups.items():
            if len(trans_list) < 2:
                continue
            
            # Sort by date
            trans_list.sort(key=lambda x: x['date'])
            
            # Calculate intervals
            intervals = []
            for i in range(1, len(trans_list)):
                date1 = datetime.fromisoformat(trans_list[i-1]['date'])
                date2 = datetime.fromisoformat(trans_list[i]['date'])
                intervals.append((date2 - date1).days)
            
            if not intervals:
                continue
            
            # Check for consistent intervals
            avg_interval = sum(intervals) / len(intervals)
            variance = sum((x - avg_interval) ** 2 for x in intervals) / len(intervals)
            
            # Detect monthly (28-31 days) or weekly (6-8 days) patterns
            is_monthly = 28 <= avg_interval <= 31 and variance < 10
            is_weekly = 6 <= avg_interval <= 8 and variance < 2
            
            if is_monthly or is_weekly:
                pattern = 'Monthly' if is_monthly else 'Weekly'
                avg_amount = sum(t['amount'] for t in trans_list) / len(trans_list)
                
                recurring.append({
                    'merchant': merchant,
                    'pattern': pattern,
                    'avg_amount': round(avg_amount, 2),
                    'count': len(trans_list),
                    'last_date': trans_list[-1]['date'],
                    'next_expected': self._calculate_next_date(trans_list[-1]['date'], avg_interval)
                })
        
        return recurring
    
    def _calculate_next_date(self, last_date, interval):
        """Calculate next expected date"""
        last = datetime.fromisoformat(last_date)
        next_date = last + timedelta(days=int(interval))
        return next_date.strftime('%Y-%m-%d')
