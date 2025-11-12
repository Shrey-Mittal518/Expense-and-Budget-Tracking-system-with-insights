"""
Unit tests for auto-detection functionality
"""
import pytest
import tempfile
import os
from services.auto_detect import AutoDetector
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
def detector(data_store):
    """Create auto detector instance"""
    return AutoDetector(data_store)

def test_normalize_merchant_amazon(detector):
    """Test merchant normalization for Amazon"""
    assert detector._normalize_merchant('AMZN MKTP US') == 'Amazon'
    assert detector._normalize_merchant('AMAZON.COM') == 'Amazon'

def test_normalize_merchant_walmart(detector):
    """Test merchant normalization for Walmart"""
    assert detector._normalize_merchant('WAL-MART #1234') == 'Walmart'
    assert detector._normalize_merchant('WM SUPERCENTER') == 'Walmart'

def test_detect_category_food(detector):
    """Test category detection for food"""
    category = detector._detect_category('Starbucks', {})
    assert category == 'Food & Dining'
    
    category = detector._detect_category('McDonald\'s', {})
    assert category == 'Food & Dining'

def test_detect_category_shopping(detector):
    """Test category detection for shopping"""
    category = detector._detect_category('Amazon', {})
    assert category == 'Shopping'
    
    category = detector._detect_category('Target', {})
    assert category == 'Shopping'

def test_detect_category_transportation(detector):
    """Test category detection for transportation"""
    category = detector._detect_category('Uber', {})
    assert category == 'Transportation'
    
    category = detector._detect_category('Shell Gas Station', {})
    assert category == 'Transportation'

def test_calculate_confidence_high(detector):
    """Test high confidence calculation"""
    confidence = detector._calculate_confidence('Amazon', 'Shopping')
    assert confidence == 'High'

def test_calculate_confidence_medium(detector):
    """Test medium confidence calculation"""
    confidence = detector._calculate_confidence('Local Store', 'Shopping')
    assert confidence == 'Medium'

def test_calculate_confidence_low(detector):
    """Test low confidence calculation"""
    confidence = detector._calculate_confidence('Unknown', 'Other')
    assert confidence == 'Low'

def test_is_online_sale_amazon(detector):
    """Test online sale detection for Amazon"""
    assert detector._is_online_sale('Amazon') == True
    assert detector._is_online_sale('AMAZON.COM') == True

def test_is_online_sale_paypal(detector):
    """Test online sale detection for PayPal"""
    assert detector._is_online_sale('PayPal') == True

def test_is_online_sale_physical_store(detector):
    """Test that physical stores are not detected as online"""
    assert detector._is_online_sale('Local Grocery Store') == False

def test_detect_recurring_monthly(data_store, detector):
    """Test detection of monthly recurring transactions"""
    user = data_store.create_user('testuser', 'test@example.com', 'password123')
    
    # Add monthly transactions
    data_store.add_transaction(user.id, -50.00, 'Netflix', 'Entertainment', '2024-01-15')
    data_store.add_transaction(user.id, -50.00, 'Netflix', 'Entertainment', '2024-02-15')
    data_store.add_transaction(user.id, -50.00, 'Netflix', 'Entertainment', '2024-03-15')
    
    recurring = detector.detect_recurring(user.id)
    
    assert len(recurring) > 0
    netflix_rec = [r for r in recurring if r['merchant'] == 'Netflix']
    assert len(netflix_rec) == 1
    assert netflix_rec[0]['pattern'] == 'Monthly'

def test_extract_date_formats(detector):
    """Test date extraction from various formats"""
    # Test YYYY-MM-DD
    date = detector._extract_date({'date': '2024-01-15'})
    assert date == '2024-01-15'
    
    # Test MM/DD/YYYY
    date = detector._extract_date({'transaction date': '01/15/2024'})
    assert date == '2024-01-15'

def test_extract_amount(detector):
    """Test amount extraction"""
    amount = detector._extract_amount({'amount': '$123.45'})
    assert amount == 123.45
    
    amount = detector._extract_amount({'debit': '50.00'})
    assert amount == 50.00

def test_extract_merchant(detector):
    """Test merchant extraction"""
    merchant = detector._extract_merchant({'merchant': 'Test Store'})
    assert merchant == 'Test Store'
    
    merchant = detector._extract_merchant({'description': 'Coffee Shop'})
    assert merchant == 'Coffee Shop'
