"""
Envelope model for budget allocation
"""

class Envelope:
    """Represents a budget envelope"""
    
    def __init__(self, id, user_id, name, allocated, spent=0, is_pooled=False):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.allocated = allocated
        self.spent = spent
        self.is_pooled = is_pooled
    
    @property
    def remaining(self):
        return self.allocated - self.spent
    
    @property
    def percentage_used(self):
        if self.allocated == 0:
            return 0
        return (self.spent / self.allocated) * 100
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'allocated': self.allocated,
            'spent': self.spent,
            'remaining': self.remaining,
            'percentage_used': self.percentage_used,
            'is_pooled': self.is_pooled
        }
    
    def __repr__(self):
        return f'<Envelope {self.name} ${self.remaining} remaining>'
