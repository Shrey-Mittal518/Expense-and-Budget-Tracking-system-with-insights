"""
Reconciliation service for matching transactions against bank statements
"""
import csv
import io
from datetime import datetime, timedelta
from difflib import SequenceMatcher

class Reconciler:
    """Match transactions against bank statements"""
    
    def __init__(self, data_store):
        self.data_store = data_store
    
    def reconcile_statement(self, file, user_id):
        """Reconcile uploaded statement against user transactions"""
        # Parse statement
        statement_transactions = self._parse_statement(file)
        
        # Get user transactions
        user_transactions = self.data_store.get_transactions(user_id)
        
        # Match transactions
        matches = []
        unmatched_statement = []
        unmatched_user = list(user_transactions)
        
        for stmt_trans in statement_transactions:
            match = self._find_best_match(stmt_trans, unmatched_user)
            
            if match:
                matches.append({
                    'statement': stmt_trans,
                    'user': match,
                    'confidence': self._calculate_match_confidence(stmt_trans, match)
                })
                unmatched_user.remove(match)
            else:
                unmatched_statement.append(stmt_trans)
        
        return {
            'matches': matches,
            'unmatched_statement': unmatched_statement,
            'unmatched_user': unmatched_user,
            'match_rate': round(len(matches) / len(statement_transactions) * 100, 1) if statement_transactions else 0
        }
    
    def _parse_statement(self, file):
        """Parse CSV statement file"""
        transactions = []
        
        content = file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(content))
        
        for row in reader:
            # Extract fields (similar to auto_detect)
            date = self._extract_date(row)
            amount = self._extract_amount(row)
            merchant = self._extract_merchant(row)
            
            if date and amount and merchant:
                transactions.append({
                    'date': date,
                    'amount': amount,
                    'merchant': merchant
                })
        
        return transactions
    
    def _find_best_match(self, stmt_trans, user_transactions):
        """Find best matching user transaction"""
        best_match = None
        best_score = 0
        
        stmt_date = datetime.fromisoformat(stmt_trans['date'])
        
        for user_trans in user_transactions:
            user_date = datetime.fromisoformat(user_trans['date'])
            
            # Date must be within 3 days
            if abs((stmt_date - user_date).days) > 3:
                continue
            
            # Amount must match closely
            amount_diff = abs(stmt_trans['amount'] - user_trans['amount'])
            if amount_diff > 0.01:
                continue
            
            # Calculate merchant similarity
            merchant_similarity = self._string_similarity(
                stmt_trans['merchant'].lower(),
                user_trans['merchant'].lower()
            )
            
            score = merchant_similarity
            
            if score > best_score and score > 0.6:
                best_score = score
                best_match = user_trans
        
        return best_match
    
    def _calculate_match_confidence(self, stmt_trans, user_trans):
        """Calculate confidence of match"""
        # Exact amount match
        amount_match = abs(stmt_trans['amount'] - user_trans['amount']) < 0.01
        
        # Date proximity
        date_diff = abs((datetime.fromisoformat(stmt_trans['date']) - 
                        datetime.fromisoformat(user_trans['date'])).days)
        
        # Merchant similarity
        merchant_sim = self._string_similarity(
            stmt_trans['merchant'].lower(),
            user_trans['merchant'].lower()
        )
        
        score = 0
        if amount_match:
            score += 40
        if date_diff == 0:
            score += 30
        elif date_diff <= 1:
            score += 20
        score += merchant_sim * 30
        
        if score >= 80:
            return 'High'
        elif score >= 60:
            return 'Medium'
        else:
            return 'Low'
    
    def _string_similarity(self, str1, str2):
        """Calculate string similarity ratio"""
        return SequenceMatcher(None, str1, str2).ratio()
    
    def _extract_date(self, row):
        """Extract date from row"""
        date_fields = ['date', 'transaction date', 'posted date', 'trans date']
        
        for field in date_fields:
            for key in row.keys():
                if field in key.lower():
                    try:
                        date_str = row[key]
                        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']:
                            try:
                                return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
                            except:
                                continue
                    except:
                        pass
        
        return None
    
    def _extract_amount(self, row):
        """Extract amount from row"""
        amount_fields = ['amount', 'debit', 'credit', 'transaction amount']
        
        for field in amount_fields:
            for key in row.keys():
                if field in key.lower():
                    try:
                        amount_str = row[key].replace('$', '').replace(',', '').strip()
                        return float(amount_str)
                    except:
                        pass
        
        return None
    
    def _extract_merchant(self, row):
        """Extract merchant from row"""
        merchant_fields = ['merchant', 'description', 'payee', 'name', 'memo']
        
        for field in merchant_fields:
            for key in row.keys():
                if field in key.lower() and row[key]:
                    return row[key]
        
        return None
