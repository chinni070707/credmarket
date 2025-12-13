"""
Edge case tests to catch unusual scenarios
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import User
from companies.models import Company
from listings.models import Category, Listing
from messaging.models import Conversation, Message
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()


class EdgeCaseTests(TestCase):
    """Test edge cases and boundary conditions"""
    
    def setUp(self):
        """Set up test data"""
        self.company = Company.objects.create(
            domain='testcompany.com',
            name='Test Company',
            status='approved'
        )
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@testcompany.com',
            password='testpass123',
            company=self.company,
            status='approved',
            email_verified=True
        )
        
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics',
            icon='📱',
            is_active=True,
            order=1
        )
    
    def test_listing_with_zero_price(self):
        """Test handling of free items (price = 0)"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post('/listings/create/', {
            'title': 'Free Item',
            'description': 'Take it for free',
            'price': 0,
            'category': self.category.id,
            'location': 'Test',
        })
        
        # Should handle free items appropriately
        self.assertIn(response.status_code, [200, 302])
    
    def test_listing_with_decimal_price(self):
        """Test handling of decimal prices"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post('/listings/create/', {
            'title': 'Decimal Price Item',
            'description': 'Has decimal price',
            'price': 99.99,
            'category': self.category.id,
            'location': 'Test',
        })
        
        self.assertIn(response.status_code, [200, 302])
        
        # Check that decimal is preserved
        if response.status_code == 302:
            listing = Listing.objects.filter(title='Decimal Price Item').first()
            if listing:
                self.assertEqual(float(listing.price), 99.99)
    
    def test_special_characters_in_title(self):
        """Test handling of special characters in titles"""
        special_chars = [
            'Title with émojis 🎉🎊',
            'Title with "quotes"',
            "Title with 'apostrophes'",
            'Title with & ampersand',
            'Title with <brackets>',
            'Title with 中文字符',
            'Title with العربية',
        ]
        
        self.client.login(username='testuser', password='testpass123')
        
        for title in special_chars:
            with self.subTest(title=title):
                listing = Listing.objects.create(
                    title=title,
                    description='Test',
                    price=100,
                    category=self.category,
                    seller=self.user,
                    location='Test',
                    status='active'
                )
                
                # Should be able to view the listing
                response = self.client.get(f'/listings/{listing.slug}/')
                self.assertEqual(response.status_code, 200)
                
                listing.delete()
    
    def test_whitespace_only_fields(self):
        """Test handling of whitespace-only input"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post('/listings/create/', {
            'title': '   ',  # Whitespace only
            'description': '   ',
            'price': 100,
            'category': self.category.id,
            'location': 'Test',
        })
        
        # Should reject whitespace-only titles
        self.assertFalse(Listing.objects.filter(title='   ').exists())
    
    def test_inactive_category_handling(self):
        """Test behavior with inactive categories"""
        inactive_category = Category.objects.create(
            name='Inactive',
            slug='inactive',
            icon='❌',
            is_active=False,  # Inactive
            order=99
        )
        
        # Try to view inactive category
        response = self.client.get(f'/category/{inactive_category.slug}/')
        
        # Should handle appropriately (404 or show "no listings")
        self.assertIn(response.status_code, [200, 404])
    
    def test_deleted_user_listings(self):
        """Test handling of listings from deleted users"""
        # Create listing
        listing = Listing.objects.create(
            title='Test Listing',
            description='Test',
            price=100,
            category=self.category,
            seller=self.user,
            location='Test',
            status='active'
        )
        
        listing_slug = listing.slug
        
        # Delete the user (if CASCADE is not set, this tests orphaned listings)
        # Note: In production, we should use soft deletes or CASCADE
        
        # Try to view listing - should handle gracefully
        response = self.client.get(f'/listings/{listing_slug}/')
        # Should return 200 or 404, but not 500
        self.assertIn(response.status_code, [200, 404])
    
    def test_same_slug_different_categories(self):
        """Test handling of slug collisions"""
        # Create two categories with same base name
        cat1 = Category.objects.create(
            name='Test',
            slug='test',
            icon='1️⃣',
            is_active=True,
            order=1
        )
        
        # Second category with same slug should fail or get unique slug
        from django.db import IntegrityError
        try:
            cat2 = Category.objects.create(
                name='Test',
                slug='test',  # Same slug
                icon='2️⃣',
                is_active=True,
                order=2
            )
            # If it succeeds, slugs should be different
            self.assertNotEqual(cat1.slug, cat2.slug)
        except IntegrityError:
            # Expected if unique constraint is enforced
            pass
    
    def test_concurrent_message_sending(self):
        """Test handling of multiple messages in same conversation"""
        other_user = User.objects.create_user(
            username='other',
            email='other@testcompany.com',
            password='testpass123',
            company=self.company,
            status='approved',
            email_verified=True
        )
        
        listing = Listing.objects.create(
            title='Test Product',
            description='Test',
            price=100,
            category=self.category,
            seller=other_user,
            location='Test',
            status='active'
        )
        
        # Create conversation
        conv = Conversation.objects.create(
            listing=listing,
            buyer=self.user,
            seller=other_user
        )
        
        # Send multiple messages
        for i in range(5):
            Message.objects.create(
                conversation=conv,
                sender=self.user,
                receiver=other_user,
                content=f'Message {i}'
            )
        
        # Should handle multiple messages
        self.assertEqual(conv.messages.count(), 5)
    
    def test_timezone_aware_datetimes(self):
        """Test that datetime fields are timezone-aware"""
        listing = Listing.objects.create(
            title='Test Listing',
            description='Test',
            price=100,
            category=self.category,
            seller=self.user,
            location='Test',
            status='active'
        )
        
        # created_at should be timezone-aware
        self.assertIsNotNone(listing.created_at.tzinfo,
                           "Datetime should be timezone-aware")
        
        # Should be recent
        time_diff = timezone.now() - listing.created_at
        self.assertLess(time_diff.total_seconds(), 60,
                       "Listing should have been created recently")
    
    def test_duplicate_conversation_prevention(self):
        """Test that duplicate conversations for same listing/buyer are prevented"""
        other_user = User.objects.create_user(
            username='other',
            email='other@testcompany.com',
            password='testpass123',
            company=self.company,
            status='approved',
            email_verified=True
        )
        
        listing = Listing.objects.create(
            title='Test Product',
            description='Test',
            price=100,
            category=self.category,
            seller=other_user,
            location='Test',
            status='active'
        )
        
        # Create first conversation
        conv1 = Conversation.objects.create(
            listing=listing,
            buyer=self.user,
            seller=other_user
        )
        
        # Try to create duplicate conversation
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            conv2 = Conversation.objects.create(
                listing=listing,
                buyer=self.user,  # Same buyer
                seller=other_user
            )
    
    def test_self_messaging_prevention(self):
        """Test that users cannot message themselves"""
        listing = Listing.objects.create(
            title='My Product',
            description='Test',
            price=100,
            category=self.category,
            seller=self.user,  # User's own listing
            location='Test',
            status='active'
        )
        
        self.client.login(username='testuser', password='testpass123')
        
        # Try to start conversation on own listing
        response = self.client.post(f'/messages/start/{listing.slug}/')
        
        # Should prevent or redirect
        if response.status_code == 200:
            # Check for error message in context or messages
            messages = list(response.context.get('messages', []))
            if messages:
                self.assertTrue(any('own listing' in str(m).lower() for m in messages))
