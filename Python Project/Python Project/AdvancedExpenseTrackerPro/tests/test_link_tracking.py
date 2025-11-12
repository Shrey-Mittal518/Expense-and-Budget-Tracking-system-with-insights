"""
Unit tests for link tracking functionality
"""
import pytest
import os
import tempfile
from datetime import datetime
from services.link_tracker import LinkTracker

@pytest.fixture
def link_tracker():
    """Create a temporary link tracker for testing"""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    
    tracker = LinkTracker(temp_db.name)
    
    yield tracker
    
    # Cleanup
    os.unlink(temp_db.name)

def test_create_tracking_link(link_tracker):
    """Test creating a tracking link"""
    tracking_id, tracking_url = link_tracker.create_tracking_link(
        user_id=1,
        merchant='Amazon',
        title='Test Product',
        amount=1000.00,
        target_url='https://amazon.in/product/123'
    )
    
    assert tracking_id is not None
    assert tracking_url == f'/track/{tracking_id}'
    assert len(tracking_id) == 36  # UUID length

def test_get_tracked_item(link_tracker):
    """Test retrieving tracked item metadata"""
    tracking_id, _ = link_tracker.create_tracking_link(
        user_id=1,
        merchant='Flipkart',
        title='Test Item',
        amount=500.00,
        target_url='https://flipkart.com/item/456'
    )
    
    item = link_tracker.get_tracked_item(tracking_id)
    
    assert item is not None
    assert item['merchant'] == 'Flipkart'
    assert item['title'] == 'Test Item'
    assert item['amount'] == 500.00
    assert item['target_url'] == 'https://flipkart.com/item/456'

def test_record_click(link_tracker):
    """Test recording a click"""
    tracking_id, _ = link_tracker.create_tracking_link(
        user_id=1,
        merchant='Amazon',
        title='Product',
        amount=1000.00,
        target_url='https://amazon.in/product'
    )
    
    link_tracker.record_click(
        tracking_id=tracking_id,
        user_id=1,
        ip='127.0.0.1',
        user_agent='Mozilla/5.0',
        referer='http://localhost:8000/offers',
        timestamp=datetime.now(),
        extra_meta='test'
    )
    
    clicks = link_tracker.get_user_clicks(1)
    assert len(clicks) > 0
    assert clicks[0]['tracking_id'] == tracking_id

def test_anonymous_click(link_tracker):
    """Test recording anonymous click (no user_id)"""
    tracking_id, _ = link_tracker.create_tracking_link(
        user_id=1,
        merchant='Amazon',
        title='Product',
        amount=1000.00,
        target_url='https://amazon.in/product'
    )
    
    link_tracker.record_click(
        tracking_id=tracking_id,
        user_id=None,  # Anonymous
        ip='127.0.0.1',
        user_agent='Mozilla/5.0',
        referer=None,
        timestamp=datetime.now(),
        extra_meta=''
    )
    
    # Should not raise error
    assert True

def test_is_safe_redirect_valid(link_tracker):
    """Test safe redirect validation for valid URLs"""
    assert link_tracker.is_safe_redirect('https://amazon.in/product') == True
    assert link_tracker.is_safe_redirect('https://www.flipkart.com/item') == True
    assert link_tracker.is_safe_redirect('https://myntra.com/fashion') == True

def test_is_safe_redirect_invalid(link_tracker):
    """Test safe redirect validation for invalid URLs"""
    assert link_tracker.is_safe_redirect('http://amazon.in/product') == False  # Not HTTPS
    assert link_tracker.is_safe_redirect('https://evil.com/phishing') == False  # Not whitelisted
    assert link_tracker.is_safe_redirect('javascript:alert(1)') == False  # XSS attempt

def test_calculate_confidence_high(link_tracker):
    """Test confidence calculation - High"""
    confidence = link_tracker.calculate_confidence('Amazon', 1000.00)
    assert confidence == 'High'

def test_calculate_confidence_medium(link_tracker):
    """Test confidence calculation - Medium"""
    confidence = link_tracker.calculate_confidence('Amazon', None)
    assert confidence == 'Medium'
    
    confidence = link_tracker.calculate_confidence('Unknown Store', 500.00)
    assert confidence == 'Medium'

def test_calculate_confidence_low(link_tracker):
    """Test confidence calculation - Low"""
    confidence = link_tracker.calculate_confidence('Unknown Store', None)
    assert confidence == 'Low'

def test_mark_click_accepted(link_tracker):
    """Test marking a click as accepted"""
    tracking_id, _ = link_tracker.create_tracking_link(
        user_id=1,
        merchant='Amazon',
        title='Product',
        amount=1000.00,
        target_url='https://amazon.in/product'
    )
    
    link_tracker.record_click(
        tracking_id=tracking_id,
        user_id=1,
        ip='127.0.0.1',
        user_agent='Mozilla/5.0',
        referer=None,
        timestamp=datetime.now(),
        extra_meta=''
    )
    
    link_tracker.mark_click_accepted(tracking_id, 1)
    
    clicks = link_tracker.get_user_clicks(1)
    assert clicks[0]['accepted_flag'] == 1

def test_get_click_stats(link_tracker):
    """Test getting click statistics"""
    # Create and click multiple items
    for i in range(3):
        tracking_id, _ = link_tracker.create_tracking_link(
            user_id=1,
            merchant=f'Store{i}',
            title=f'Product{i}',
            amount=1000.00,
            target_url=f'https://amazon.in/product{i}'
        )
        
        link_tracker.record_click(
            tracking_id=tracking_id,
            user_id=1,
            ip='127.0.0.1',
            user_agent='Mozilla/5.0',
            referer=None,
            timestamp=datetime.now(),
            extra_meta=''
        )
    
    # Accept one
    clicks = link_tracker.get_user_clicks(1)
    link_tracker.mark_click_accepted(clicks[0]['tracking_id'], 1)
    
    stats = link_tracker.get_click_stats(1)
    assert stats['total_clicks'] == 3
    assert stats['accepted_clicks'] == 1
    assert stats['unique_items'] == 3

def test_multiple_clicks_same_item(link_tracker):
    """Test multiple clicks on the same tracking link"""
    tracking_id, _ = link_tracker.create_tracking_link(
        user_id=1,
        merchant='Amazon',
        title='Product',
        amount=1000.00,
        target_url='https://amazon.in/product'
    )
    
    # Click twice
    for _ in range(2):
        link_tracker.record_click(
            tracking_id=tracking_id,
            user_id=1,
            ip='127.0.0.1',
            user_agent='Mozilla/5.0',
            referer=None,
            timestamp=datetime.now(),
            extra_meta=''
        )
    
    clicks = link_tracker.get_user_clicks(1)
    assert len(clicks) == 2
    assert all(c['tracking_id'] == tracking_id for c in clicks)
