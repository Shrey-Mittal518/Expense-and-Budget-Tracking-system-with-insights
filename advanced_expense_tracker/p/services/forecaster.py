"""
Rule-based forecasting engine for balance projection
No ML - uses historical patterns and recurring transactions
"""
from datetime import datetime, timedelta
from collections import defaultdict

class Forecaster:
    """Balance forecasting using rule-based analysis"""
    
    def __init__(self, data_store):
        self.data_store = data_store
    
    def forecast_balance(self, user_id, days=30):
        """Project balance over N days based on historical data"""
        transactions = self.data_store.get_transactions(user_id)
        
        if not transactions:
            return {
                'current_balance': 0,
                'projected_balance': 0,
                'daily_projections': [],
                'confidence': 'Low'
            }
        
        # Calculate current balance
        current_balance = sum(t['amount'] for t in transactions)
        
        # Analyze spending patterns
        daily_avg = self._calculate_daily_average(transactions)
        
        # Get recurring transactions
        from services.auto_detect import AutoDetector
        detector = AutoDetector(self.data_store)
        recurring = detector.detect_recurring(user_id)
        
        # Project daily balances
        daily_projections = []
        projected_balance = current_balance
        
        for day in range(days):
            date = (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d')
            
            # Apply daily average spending
            projected_balance -= daily_avg
            
            # Check for recurring transactions
            for rec in recurring:
                if rec['next_expected'] == date:
                    projected_balance += rec['avg_amount']
            
            daily_projections.append({
                'date': date,
                'balance': round(projected_balance, 2)
            })
        
        # Calculate confidence based on data quality
        confidence = self._calculate_forecast_confidence(transactions, recurring)
        
        return {
            'current_balance': round(current_balance, 2),
            'projected_balance': round(projected_balance, 2),
            'daily_projections': daily_projections,
            'daily_avg_spending': round(daily_avg, 2),
            'confidence': confidence
        }
    
    def _calculate_daily_average(self, transactions):
        """Calculate average daily spending"""
        if not transactions:
            return 0
        
        # Filter expenses (negative amounts)
        expenses = [t for t in transactions if t['amount'] < 0]
        
        if not expenses:
            return 0
        
        # Get date range
        dates = [datetime.fromisoformat(t['date']) for t in expenses]
        date_range = (max(dates) - min(dates)).days or 1
        
        total_spent = sum(abs(t['amount']) for t in expenses)
        return total_spent / date_range
    
    def _calculate_forecast_confidence(self, transactions, recurring):
        """Calculate confidence level for forecast"""
        score = 0
        
        # More transactions = higher confidence
        if len(transactions) > 50:
            score += 40
        elif len(transactions) > 20:
            score += 25
        elif len(transactions) > 5:
            score += 10
        
        # Recurring patterns increase confidence
        score += min(len(recurring) * 10, 30)
        
        # Recent data increases confidence
        recent = [t for t in transactions 
                 if (datetime.now() - datetime.fromisoformat(t['date'])).days < 30]
        if len(recent) > 10:
            score += 30
        
        if score >= 70:
            return 'High'
        elif score >= 40:
            return 'Medium'
        else:
            return 'Low'
    
    def analyze_spending_trends(self, user_id):
        """Analyze spending trends by category and merchant"""
        transactions = self.data_store.get_transactions(user_id)
        
        # Group by category
        category_totals = defaultdict(float)
        merchant_totals = defaultdict(float)
        monthly_totals = defaultdict(float)
        
        for t in transactions:
            if t['amount'] < 0:  # Expenses only
                category_totals[t['category']] += abs(t['amount'])
                merchant_totals[t['merchant']] += abs(t['amount'])
                
                # Monthly grouping
                month = datetime.fromisoformat(t['date']).strftime('%Y-%m')
                monthly_totals[month] += abs(t['amount'])
        
        # Top categories
        top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Top merchants
        top_merchants = sorted(merchant_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Monthly trend
        monthly_trend = sorted(monthly_totals.items())
        
        return {
            'top_categories': [{'name': k, 'amount': round(v, 2)} for k, v in top_categories],
            'top_merchants': [{'name': k, 'amount': round(v, 2)} for k, v in top_merchants],
            'monthly_trend': [{'month': k, 'amount': round(v, 2)} for k, v in monthly_trend]
        }
    
    def detect_budget_breach(self, user_id, envelope_id):
        """Explain why an envelope budget was breached"""
        envelope = None
        envelopes = self.data_store.get_envelopes(user_id)
        
        for env in envelopes:
            if env['id'] == envelope_id:
                envelope = env
                break
        
        if not envelope or envelope['spent'] <= envelope['allocated']:
            return None
        
        # Get transactions for this envelope
        transactions = [t for t in self.data_store.get_transactions(user_id) 
                       if t.get('envelope_id') == envelope_id]
        
        # Analyze breach
        overage = envelope['spent'] - envelope['allocated']
        
        # Find largest transactions
        largest = sorted(transactions, key=lambda x: abs(x['amount']), reverse=True)[:3]
        
        # Category breakdown
        category_totals = defaultdict(float)
        for t in transactions:
            category_totals[t['category']] += abs(t['amount'])
        
        return {
            'envelope_name': envelope['name'],
            'overage': round(overage, 2),
            'percentage_over': round((overage / envelope['allocated']) * 100, 2),
            'largest_transactions': [
                {'merchant': t['merchant'], 'amount': abs(t['amount']), 'date': t['date']}
                for t in largest
            ],
            'category_breakdown': [
                {'category': k, 'amount': round(v, 2)}
                for k, v in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
            ],
            'suggestion': self._generate_breach_suggestion(envelope, overage, category_totals)
        }
    
    def _generate_breach_suggestion(self, envelope, overage, category_totals):
        """Generate actionable suggestion for budget breach"""
        top_category = max(category_totals.items(), key=lambda x: x[1])[0] if category_totals else None
        
        suggestions = []
        
        if overage / envelope['allocated'] > 0.5:
            suggestions.append(f"Consider increasing the '{envelope['name']}' budget by at least ${round(overage, 2)}")
        
        if top_category:
            suggestions.append(f"'{top_category}' is the largest spending category - look for savings here")
        
        suggestions.append("Review recent transactions for unnecessary expenses")
        
        return ' | '.join(suggestions)
