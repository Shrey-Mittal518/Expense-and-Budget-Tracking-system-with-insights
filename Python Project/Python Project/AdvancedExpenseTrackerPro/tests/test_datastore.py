"""
Unit tests for data store functionality
"""
import pytest
import os
import tempfile
from services.data_store import DataStore

@pytest.fixture
def data_store():
    """Create a temporary data store for testing"""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_dir = tempfile.mkdtemp()
    
    ds = DataStore(temp_db.name, temp_dir)
    ds.init_db()
    
    yield ds
    
    # Cleanup
    os.unlink(temp_db.name)
    for file in os.listdir(temp_dir):
        os.unlink(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)

def test_create_user(data_store):
    """Test user creation"""
    user = data_store.create_user('testuser', 'test@example.com', 'password123', True)
    
    assert user is not None
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.auto_detect_enabled == True

def test_duplicate_email(data_store):
    """Test that duplicate emails are rejected"""
    data_store.create_user('user1', 'test@example.com', 'password123')
    user2 = data_store.create_user('user2', 'test@example.com', 'password456')
    
    assert user2 is None

def test_authenticate_user(data_store):
    """Test user authentication"""
    data_store.create_user('testuser', 'test@example.com', 'password123')
    
    # Correct credentials
    user = data_store.authenticate_user('test@example.com', 'password123')
    assert user is not None
    assert user.username == 'testuser'
    
    # Wrong password
    user = data_store.authenticate_user('test@example.com', 'wrongpassword')
    assert user is None

def test_add_transaction(data_store):
    """Test adding transactions"""
    user = data_store.create_user('testuser', 'test@example.com', 'password123')
    
    transaction_id = data_store.add_transaction(
        user_id=user.id,
        amount=-50.00,
        merchant='Test Store',
        category='Shopping',
        date='2024-01-15'
    )
    
    assert transaction_id is not None
    
    transactions = data_store.get_transactions(user.id)
    assert len(transactions) == 1
    assert transactions[0]['merchant'] == 'Test Store'
    assert transactions[0]['amount'] == -50.00

def test_create_envelope(data_store):
    """Test envelope creation"""
    user = data_store.create_user('testuser', 'test@example.com', 'password123')
    
    data_store.create_envelope(user.id, 'Groceries', 500.00, False)
    
    envelopes = data_store.get_envelopes(user.id)
    assert len(envelopes) == 1
    assert envelopes[0]['name'] == 'Groceries'
    assert envelopes[0]['allocated'] == 500.00

def test_transfer_envelope_funds(data_store):
    """Test transferring funds between envelopes"""
    user = data_store.create_user('testuser', 'test@example.com', 'password123')
    
    data_store.create_envelope(user.id, 'Envelope A', 500.00)
    data_store.create_envelope(user.id, 'Envelope B', 300.00)
    
    envelopes = data_store.get_envelopes(user.id)
    env_a_id = envelopes[0]['id']
    env_b_id = envelopes[1]['id']
    
    data_store.transfer_envelope_funds(env_a_id, env_b_id, 100.00, user.id)
    
    envelopes = data_store.get_envelopes(user.id)
    assert envelopes[0]['allocated'] == 400.00
    assert envelopes[1]['allocated'] == 400.00

def test_user_file_creation(data_store):
    """Test that user transaction file is created"""
    user = data_store.create_user('testuser', 'test@example.com', 'password123')
    
    user_file = data_store._get_user_file_path(user.id)
    assert os.path.exists(user_file)

def test_transaction_appended_to_file(data_store):
    """Test that transactions are appended to user file"""
    user = data_store.create_user('testuser', 'test@example.com', 'password123')
    
    data_store.add_transaction(
        user_id=user.id,
        amount=-25.00,
        merchant='Coffee Shop',
        category='Food & Dining',
        date='2024-01-15'
    )
    
    user_file = data_store._get_user_file_path(user.id)
    with open(user_file, 'r') as f:
        content = f.read()
        assert 'Coffee Shop' in content
        assert '-25.0' in content
