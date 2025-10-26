# benchmarking.py
import pandas as pd
from datetime import datetime, timedelta

DATA_FILE = "family_expenses_10000.csv"

def get_spending_comparison(family_id):
    """Compare current month spending with previous month"""
    try:
        df = pd.read_csv(DATA_FILE)
        df = df[df['Family_ID'] == family_id]
        
        if df.empty:
            return None
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Get current month and previous month
        today = datetime.now()
        current_month_start = today.replace(day=1)
        previous_month_end = current_month_start - timedelta(days=1)
        previous_month_start = previous_month_end.replace(day=1)
        
        # Filter data for current and previous month
        current_month_df = df[df['Date'] >= current_month_start]
        previous_month_df = df[(df['Date'] >= previous_month_start) & (df['Date'] < current_month_start)]
        
        if previous_month_df.empty:
            return {
                'message': "No previous month data available for comparison",
                'status': 'info',
                'details': {}
            }
        
        # Get spending by category
        current_spending = current_month_df.groupby('Category')['Amount'].sum().to_dict()
        previous_spending = previous_month_df.groupby('Category')['Amount'].sum().to_dict()
        
        # Calculate total spending
        current_total = sum(current_spending.values())
        previous_total = sum(previous_spending.values())
        
        comparisons = {}
        
        # Compare each category
        all_categories = set(list(current_spending.keys()) + list(previous_spending.keys()))
        
        for category in all_categories:
            current_amount = current_spending.get(category, 0)
            previous_amount = previous_spending.get(category, 0)
            
            if previous_amount > 0:
                diff = ((current_amount - previous_amount) / previous_amount) * 100
                comparisons[category] = {
                    'current': current_amount,
                    'previous': previous_amount,
                    'diff_percent': round(diff, 1),
                    'diff_amount': current_amount - previous_amount
                }
        
        # Overall comparison
        if previous_total > 0:
            total_diff_percent = ((current_total - previous_total) / previous_total) * 100
            
            if total_diff_percent < -5:
                message = f"Great job! You spent {abs(round(total_diff_percent, 1))}% less than last month 🎉"
                status = "success"
            elif total_diff_percent > 5:
                message = f"You spent {round(total_diff_percent, 1)}% more than last month ⚠️"
                status = "warning"
            else:
                message = f"Your spending is similar to last month ({round(total_diff_percent, 1):+.1f}%)"
                status = "info"
        else:
            message = "This is your first month tracking expenses"
            status = "info"
        
        return {
            'message': message,
            'status': status,
            'current_total': current_total,
            'previous_total': previous_total,
            'details': comparisons
        }
    
    except Exception as e:
        print(f"Error in benchmarking: {e}")
        return None
