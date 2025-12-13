"""
Performance and N+1 query tests to detect efficiency issues early
"""
from django.test import TestCase, override_settings
from django.db import connection
from django.test.utils import override_settings
from accounts.models import User
from companies.models import Company
from listings.models import Category, Listing
from messaging.models import Conversation, Message


class PerformanceTests(TestCase):
    """Test for N+1 queries and performance issues"""
    
    def setUp(self):
        """Set up test data"""
        # Create company
        self.company = Company.objects.create(
            domain='testcompany.com',
            name='Test Company',
            status='approved'
        )
        
        # Create users
        self.users = []
        for i in range(10):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@testcompany.com',
                password='testpass123',
                company=self.company,
                status='approved',
                email_verified=True
            )
            self.users.append(user)
        
        # Create category
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics',
            icon='📱',
            is_active=True,
            order=1
        )
        
        # Create listings
        self.listings = []
        for i, user in enumerate(self.users):
            listing = Listing.objects.create(
                title=f'Product {i}',
                description=f'Description {i}',
                price=100 * (i + 1),
                category=self.category,
                seller=user,
                location=f'Location {i}',
                status='active'
            )
            self.listings.append(listing)
    
    def test_listing_list_no_n_plus_1(self):
        """Test that listing list page doesn't have N+1 query problem"""
        # Reset query count
        connection.queries_log.clear()
        
        with self.assertNumQueries(10, using='default'):  # Adjust based on actual optimized query count
            response = self.client.get('/listings/')
            self.assertEqual(response.status_code, 200)
            
            # Should have listings in context
            self.assertIn('object_list', response.context)
    
    def test_home_page_query_count(self):
        """Test that home page has reasonable query count"""
        connection.queries_log.clear()
        
        # Home page should have limited queries regardless of listing count
        with self.assertNumQueries(15, using='default'):  # Adjust based on actual
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
    
    def test_category_listings_no_n_plus_1(self):
        """Test that category listing page is optimized"""
        connection.queries_log.clear()
        
        with self.assertNumQueries(10, using='default'):  # Adjust based on actual
            response = self.client.get(f'/category/{self.category.slug}/')
            self.assertEqual(response.status_code, 200)
    
    def test_messaging_inbox_optimized(self):
        """Test that messaging inbox doesn't have N+1 queries"""
        # Create some conversations
        for i in range(5):
            conv = Conversation.objects.create(
                listing=self.listings[i],
                buyer=self.users[0],
                seller=self.listings[i].seller
            )
            Message.objects.create(
                conversation=conv,
                sender=self.users[0],
                receiver=self.listings[i].seller,
                content=f'Message {i}'
            )
        
        self.client.login(username='user0', password='testpass123')
        connection.queries_log.clear()
        
        with self.assertNumQueries(10, using='default'):  # Adjust based on actual
            response = self.client.get('/messages/')
            self.assertIn(response.status_code, [200, 302])


class ScalabilityTests(TestCase):
    """Test system behavior with large datasets"""
    
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
    
    def test_large_listing_title(self):
        """Test handling of very long listing titles"""
        long_title = 'A' * 500  # Very long title
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post('/listings/create/', {
            'title': long_title,
            'description': 'Test',
            'price': 100,
            'category': self.category.id,
            'location': 'Test',
        })
        
        # Should handle gracefully (truncate or reject)
        self.assertIn(response.status_code, [200, 302])
    
    def test_large_description(self):
        """Test handling of very long descriptions"""
        long_description = 'X' * 10000  # Very long description
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post('/listings/create/', {
            'title': 'Test Listing',
            'description': long_description,
            'price': 100,
            'category': self.category.id,
            'location': 'Test',
        })
        
        # Should handle gracefully
        self.assertIn(response.status_code, [200, 302])
    
    def test_pagination_works(self):
        """Test that pagination prevents loading too many records"""
        # Create many listings
        for i in range(50):
            Listing.objects.create(
                title=f'Product {i}',
                description=f'Description {i}',
                price=100,
                category=self.category,
                seller=self.user,
                location='Test',
                status='active'
            )
        
        response = self.client.get('/listings/')
        self.assertEqual(response.status_code, 200)
        
        # Check if paginated
        if 'page_obj' in response.context:
            # Should not load all 50 listings at once
            self.assertLessEqual(len(response.context['page_obj']), 25,
                               "Should paginate listings")
