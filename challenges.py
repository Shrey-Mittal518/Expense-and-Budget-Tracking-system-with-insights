# challenges.py
import pandas as pd
import json
import os
from datetime import datetime

CHALLENGES_FILE = "user_challenges.json"
DATA_FILE = "family_expenses_10000.csv"

# Available challenges
AVAILABLE_CHALLENGES = {
    'no_spend_day': {
        'name': 'No-Spend Day Challenge',
        'description': 'Complete 5 days without any expenses',
        'target': 5,
        'reward': '⭐ Budget Master Badge',
        'points': 100
    },
    'save_5000': {
        'name': 'Save ₹5000 Challenge',
        'description': 'Keep your monthly spending under budget to save ₹5000',
        'target': 5000,
        'reward': '💰 Savings Champion',
        'points': 200
    },
    'category_limit': {
        'name': 'Category Budget Challenge',
        'description': 'Stay within budget for Food category (₹8000)',
        'target': 8000,
        'reward': '🍔 Food Budget Hero',
        'points': 150
    }
}

def load_challenges():
    """Load user challenges from file"""
    if os.path.exists(CHALLENGES_FILE):
        with open(CHALLENGES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_challenges(challenges):
    """Save challenges to file"""
    with open(CHALLENGES_FILE, 'w') as f:
        json.dump(challenges, f, indent=2)

def get_user_challenges(user_id):
    """Get challenges for a specific user"""
    challenges = load_challenges()
    
    if user_id not in challenges:
        # Initialize new user with all challenges
        challenges[user_id] = {
            'active_challenges': [],
            'completed_challenges': [],
            'total_points': 0
        }
        save_challenges(challenges)
    
    return challenges[user_id]

def activate_challenge(user_id, challenge_id):
    """Activate a challenge for user"""
    challenges = load_challenges()
    
    if user_id not in challenges:
        challenges[user_id] = {
            'active_challenges': [],
            'completed_challenges': [],
            'total_points': 0
        }
    
    if challenge_id in AVAILABLE_CHALLENGES:
        challenge_data = AVAILABLE_CHALLENGES[challenge_id].copy()
        challenge_data['id'] = challenge_id
        challenge_data['progress'] = 0
        challenge_data['started_at'] = datetime.now().strftime('%Y-%m-%d')
        
        challenges[user_id]['active_challenges'].append(challenge_data)
        save_challenges(challenges)
        return True
    
    return False

def check_challenge_progress(user_id, family_id):
    """Check and update challenge progress"""
    challenges = load_challenges()
    
    if user_id not in challenges:
        return []
    
    user_challenges = challenges[user_id]
    df = pd.read_csv(DATA_FILE)
    df = df[df['Family_ID'] == family_id]
    
    completed = []
    
    for challenge in user_challenges['active_challenges']:
        challenge_id = challenge['id']
        
        if challenge_id == 'no_spend_day':
            # Count days with zero expenses
            df['Date'] = pd.to_datetime(df['Date'])
            all_dates = pd.date_range(start=df['Date'].min(), end=df['Date'].max())
            expense_dates = df['Date'].dt.date.unique()
            no_spend_days = len([d for d in all_dates if d.date() not in expense_dates])
            challenge['progress'] = no_spend_days
            
            if no_spend_days >= challenge['target']:
                completed.append(challenge)
        
        elif challenge_id == 'save_5000':
            # Check if total spending allows for ₹5000 savings
            total_spent = df['Amount'].sum()
            # Assuming monthly income of ₹50000
            savings = 50000 - total_spent
            challenge['progress'] = max(0, savings)
            
            if savings >= challenge['target']:
                completed.append(challenge)
        
        elif challenge_id == 'category_limit':
            # Check Food category spending
            food_spending = df[df['Category'] == 'Food']['Amount'].sum()
            challenge['progress'] = challenge['target'] - food_spending
            
            if food_spending <= challenge['target']:
                completed.append(challenge)
    
    # Move completed challenges
    for completed_challenge in completed:
        user_challenges['active_challenges'].remove(completed_challenge)
        user_challenges['completed_challenges'].append(completed_challenge)
        user_challenges['total_points'] += completed_challenge['points']
    
    challenges[user_id] = user_challenges
    save_challenges(challenges)
    
    return completed
