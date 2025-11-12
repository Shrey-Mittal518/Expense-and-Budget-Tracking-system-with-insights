"""
Unit tests for forecasting functionality
"""
import pytest
import tempfile
import os
from datetime import datetime, timedelta
from services.forecaster import Forecaster
from services.data_store import DataStore

@pytest.fixture
def data_store():
    """Create a temporary data store for testing"""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_dir = tempfile.mkdtemp()
    
    ds = DataStore(temp_db.name, temp_dir)
    ds.init_db()
    
    yield ds
    
    os.unlink(temp_db.name)
    for file in os.listdir(temp_dir):
        os.unlink(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)

@pytest.fixture
def forecaster(data_store):
    """Create forecaster instance"""
    return Forecaster(data_store)

def test_forecast_empty_data(data_store, forecaster):
    """Test forecast with no transactions"""
    user = data_store.create_user('testuser', 'test@example.com', 'password123')
    
    forecast = forecaster.forecast_balance(user.id, days=30)
    
    assert forecast['current_balance'] == 0
    assert forecast['projected_balance'] == 0
    assert forecast['confidence'] == 'Low'

def test_forecast_with_transactions(data_store, forecaster):
    """Test forecast with transaction history"""
    user = data_store.create_user('testuser', 'test@example.com', 'password123')
    
    # Add some transactions
    today = datetime.now()
    for i in range(10):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        data_store.add_transaction(user.id, -10.00, f'Store {i}', 'Shopping', date)
    
    forecast = forecaster.forecast_balance(user.id, days=30)
    
    assert forecast['current_balance'] == -100.00
    assert len(forecast['daily_projections']) == 30
    assert forecast['confidence'] in ['Low', 'Medium', 'High']

def test_calculate_daily_average(data_store, forecaster):
    """Test daily average calculation"""
    user = data_store.create_user('testuser', 'test@example.com', 'password123')
    
    # Add transactions over 10 days
    today = datetime.now()
    for i in range(10):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        data_store.add_transaction(user.id, -10.00, 'Store', 'Shopping', date)
    
    transactions = data_store.get_transactions(user.id)
    daily_avg = forecaster._calculate_daily_average(transactions)
    
    assert daily_avg > 0  # Should have positive daily spending

def test_analyze_spending_trends(data_store, forecaster):
    """Test spending trend analysis"""
    user = data_store.create_user('testuser', 'test@example.com', 'password123')
    
    # Add transactions in different categories
    data_store.add_transaction(user.id, -50.00, 'Grocery Store', 'Food & Dining', '2024-01-15')
    data_store.add_transaction(user.id, -30.00, 'Amazon', 'Shopping', '2024-01-16')
    data_store.add_transaction(user.id, -20.00, 'Gas Station', 'Transportation', '2024-01-17')
    
    trends = forecaster.analyze_spending_trends(user.id)
    
    assert 'top_categories' in trends
    assert 'top_merchants' in trends
    assert len(trends['top_categories']) > 0

def test_forecast_confidence_high(data_store, forecaster):
    """Test high confidence forecast"""
    user = data_store.create_user('testuser', 'test@example.com', 'password123')
    
    # Add many recent transactions
    today = datetime.now()
    for i in range(60):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        data_store.add_transaction(user.id, -10.00, 'Store', 'Shopping', date)
    
    forecast = forecaster.forecast_balance(user.id, days=30)
    
    assert forecast['confidence'] == 'High'

def test_detect_budget_breach(data_store, forecaster):
    """Test budget breach detection"""
    user = data_store.create_user('testuser', 'test@example.com', 'password123')
    
    # Create envelope
    data_store.create_envelope(user.id, 'Groceries', 100.00)
    envelopes = data_store.get_envelopes(user.id)
    envelope_id = envelopes[0]['id']
    
    # Add transactions that exceed budget
    data_store.add_transaction(user.id, -60.00, 'Store 1', 'Food & Dining', '2024-01-15', envelope_id)
    data_store.add_transaction(user.id, -60.00, 'Store 2', 'Food & Dining', '2024-01-16', envelope_id)
    
    breach = forecaster.detect_budget_breach(user.id, envelope_id)
    
    assert breach is not None
    assert breach['overage'] > 0
    assert 'suggestion' in breach
