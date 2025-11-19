"""
Transaction model
"""
from datetime import datetime

class Transaction:
    """Represents a financial transaction"""
    
    def __init__(self, id, user_id, amount, merchant, category, date, 
                 envelope_id=None, notes='', is_online_sale=False):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.merchant = merchant
        self.category = category
        self.date = date if isinstance(date, datetime) else datetime.fromisoformat(date)
        self.envelope_id = envelope_id
        self.notes = notes
        self.is_online_sale = is_online_sale
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'merchant': self.merchant,
            'category': self.category,
            'date': self.date.isoformat(),
            'envelope_id': self.envelope_id,
            'notes': self.notes,
            'is_online_sale': self.is_online_sale
        }
    
    def __repr__(self):
        return f'<Transaction {self.merchant} ${self.amount}>'
