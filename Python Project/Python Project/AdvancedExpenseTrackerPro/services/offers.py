"""
Offers management system for discounts and promotions
"""
import json
import os
from datetime import datetime

class OffersManager:
    """Manage discount offers and promotions"""
    
    # Popular shopping sites with their offers
    SHOPPING_SITES = {
        'Amazon': {
            'url': 'https://www.amazon.in/deals',
            'logo': '🛒',
            'color': '#FF9900',
            'offers': [
                {'title': 'Great Indian Festival', 'discount': '50-80%', 'category': 'Electronics'},
                {'title': 'Daily Deals', 'discount': 'Up to 70%', 'category': 'Fashion'},
                {'title': 'Lightning Deals', 'discount': 'Limited Time', 'category': 'All'}
            ]
        },
        'Flipkart': {
            'url': 'https://www.flipkart.com/offers-store',
            'logo': '🛍️',
            'color': '#2874F0',
            'offers': [
                {'title': 'Big Billion Days', 'discount': '50-90%', 'category': 'All'},
                {'title': 'Fashion Sale', 'discount': 'Up to 80%', 'category': 'Fashion'},
                {'title': 'Electronics Fest', 'discount': 'Up to 75%', 'category': 'Electronics'}
            ]
        },
        'Myntra': {
            'url': 'https://www.myntra.com/sale',
            'logo': '👗',
            'color': '#FF3F6C',
            'offers': [
                {'title': 'End of Season Sale', 'discount': '40-80%', 'category': 'Fashion'},
                {'title': 'Brand Fest', 'discount': 'Up to 70%', 'category': 'Brands'},
                {'title': 'Clearance Sale', 'discount': 'Up to 90%', 'category': 'All'}
            ]
        },
        'Swiggy': {
            'url': 'https://www.swiggy.com/offers',
            'logo': '🍔',
            'color': '#FC8019',
            'offers': [
                {'title': 'Free Delivery', 'discount': '₹0 Delivery', 'category': 'Food'},
                {'title': 'Bank Offers', 'discount': '20% Off', 'category': 'Food'},
                {'title': 'Super Saver', 'discount': 'Up to 60%', 'category': 'Food'}
            ]
        },
        'Zomato': {
            'url': 'https://www.zomato.com/offers',
            'logo': '🍕',
            'color': '#E23744',
            'offers': [
                {'title': 'Zomato Gold', 'discount': '1+1 Free', 'category': 'Food'},
                {'title': 'Pro Membership', 'discount': 'Extra 10%', 'category': 'Food'},
                {'title': 'Weekend Special', 'discount': 'Up to 50%', 'category': 'Food'}
            ]
        },
        'Paytm': {
            'url': 'https://paytm.com/offers',
            'logo': '💳',
            'color': '#00BAF2',
            'offers': [
                {'title': 'Cashback Offers', 'discount': 'Up to ₹500', 'category': 'All'},
                {'title': 'Bill Payments', 'discount': '10% Cashback', 'category': 'Bills'},
                {'title': 'Recharge Offers', 'discount': '₹50 Cashback', 'category': 'Mobile'}
            ]
        }
    }
    
    def __init__(self, offers_file='data/offers.json'):
        self.offers_file = offers_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create offers file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.offers_file), exist_ok=True)
        if not os.path.exists(self.offers_file):
            with open(self.offers_file, 'w') as f:
                json.dump([], f)
    
    def get_offers(self, user_id):
        """Get all offers for user"""
        with open(self.offers_file, 'r') as f:
            all_offers = json.load(f)
        
        # Filter by user and check expiry
        active_offers = []
        for offer in all_offers:
            if offer['user_id'] == user_id:
                if not offer.get('expiry') or datetime.fromisoformat(offer['expiry']) > datetime.now():
                    active_offers.append(offer)
        
        return active_offers
    
    def add_offer(self, user_id, merchant, discount, description, expiry=None):
        """Add new offer"""
        with open(self.offers_file, 'r') as f:
            offers = json.load(f)
        
        new_offer = {
            'id': len(offers) + 1,
            'user_id': user_id,
            'merchant': merchant,
            'discount': discount,
            'description': description,
            'expiry': expiry,
            'created_at': datetime.now().isoformat()
        }
        
        offers.append(new_offer)
        
        with open(self.offers_file, 'w') as f:
            json.dump(offers, f, indent=2)
        
        return new_offer
    
    def apply_offer_to_transaction(self, transaction, offers):
        """Apply matching offer to transaction"""
        merchant = transaction['merchant'].lower()
        
        for offer in offers:
            if offer['merchant'].lower() in merchant:
                discount_amount = transaction['amount'] * (offer['discount'] / 100)
                return {
                    'original_amount': transaction['amount'],
                    'discount': discount_amount,
                    'final_amount': transaction['amount'] - discount_amount,
                    'offer_description': offer['description']
                }
        
        return None
    
    def get_potential_savings(self, user_id, transactions):
        """Calculate potential savings from available offers"""
        offers = self.get_offers(user_id)
        total_savings = 0
        
        for transaction in transactions:
            result = self.apply_offer_to_transaction(transaction, offers)
            if result:
                total_savings += result['discount']
        
        return round(total_savings, 2)
    
    def get_live_offers(self):
        """Get live offers from popular shopping sites"""
        return self.SHOPPING_SITES
    
    def get_site_by_merchant(self, merchant):
        """Get shopping site info based on merchant name"""
        merchant_lower = merchant.lower()
        
        for site_name, site_info in self.SHOPPING_SITES.items():
            if site_name.lower() in merchant_lower:
                return site_name, site_info
        
        return None, None
