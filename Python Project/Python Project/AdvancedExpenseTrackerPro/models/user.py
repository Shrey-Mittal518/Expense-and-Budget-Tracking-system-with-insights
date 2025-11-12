"""
User model for authentication
"""
from flask_login import UserMixin

class User(UserMixin):
    """User model with Flask-Login integration"""
    
    def __init__(self, id, username, email, auto_detect_enabled=False):
        self.id = id
        self.username = username
        self.email = email
        self.auto_detect_enabled = auto_detect_enabled
    
    def get_id(self):
        return str(self.id)
    
    def __repr__(self):
        return f'<User {self.username}>'
