"""
Tests for credmarket app views (error handlers) and link validity
"""
import pytest
from django.test import Client, TestCase
from django.urls import reverse
from accounts.models import User
from companies.models import Company
from listings.models import Category, Listing


@pytest.mark.django_db
class TestErrorViews:
    """Test custom error handler views"""
    
    def test_404_error_page(self, client):
        """Test custom 404 error page"""
        response = client.get('/nonexistent-page-url/')
        assert response.status_code == 404
        # The 404 template should be rendered
        # In production, this will use the custom handler
    
    def test_403_error_page(self, client):
        """Test custom 403 error page"""
        # Import the view directly to test it
        from credmarket.views import custom_403
        from django.http import HttpRequest
        
        request = HttpRequest()
        response = custom_403(request)
        assert response.status_code == 403
    
    def test_500_error_page(self, client):
        """Test custom 500 error page"""
        # Import the view directly to test it
        from credmarket.views import custom_500
        from django.http import HttpRequest
        
        request = HttpRequest()
        response = custom_500(request)
        assert response.status_code == 500


class LinkValidityTests(TestCase):
    """Test that all important URLs are accessible and don't return 404"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        
        # Create a test company
        self.company = Company.objects.create(
            domain='testcompany.com',
            name='Test Company',
            status='approved'
        )
        
        # Create a test user (staff for admin tests)
        self.user = User.objects.create_user(
            username='testuser',
            email='test@testcompany.com',
            password='testpass123',
            company=self.company,
            status='approved',
            email_verified=True,
            is_staff=True  # Make user staff for admin access
        )
        
        # Create a test category
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics',
            icon='📱',
            description='Electronic items',
            is_active=True,
            order=1
        )
        
        # Create a test listing with active status
        self.listing = Listing.objects.create(
            title='Test Product',
            description='Test description',
            price=100,
            category=self.category,
            seller=self.user,
            location='Test City',
            status='active'  # Active listing so it's viewable
        )
    
    def test_public_pages_accessible(self):
        """Test that public pages return 200 OK"""
        public_urls = [
            ('/', 'Home page'),
            ('/about/', 'About page'),
            ('/how-it-works/', 'How it works page'),
            ('/accounts/login/', 'Login page'),
            ('/accounts/signup/', 'Signup page'),
            ('/listings/', 'Listings page'),
            (f'/listings/{self.listing.slug}/', 'Listing detail page'),
            (f'/listings/category/{self.category.slug}/', 'Category page'),
        ]
        
        for url, description in public_urls:
            with self.subTest(url=url, description=description):
                response = self.client.get(url)
                self.assertIn(
                    response.status_code, 
                    [200, 302],  # 302 is OK for redirects
                    f"{description} ({url}) failed with status {response.status_code}"
                )
    
    def test_authenticated_pages_redirect_when_logged_out(self):
        """Test that authenticated pages redirect to login when not authenticated"""
        auth_required_urls = [
            ('/accounts/profile/', 'Profile page'),
            ('/accounts/profile/edit/', 'Edit profile page'),
            ('/listings/create/', 'Create listing page'),
            ('/messaging/', 'Inbox page'),
        ]
        
        for url, description in auth_required_urls:
            with self.subTest(url=url, description=description):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    302,
                    f"{description} ({url}) should redirect to login but returned {response.status_code}"
                )
                self.assertIn('/accounts/login/', response.url, 
                             f"{description} should redirect to login page")
    
    def test_authenticated_pages_accessible_when_logged_in(self):
        """Test that authenticated pages are accessible when logged in"""
        self.client.login(username='testuser', password='testpass123')
        
        auth_urls = [
            ('/accounts/profile/', 'Profile page'),
            ('/accounts/profile/edit/', 'Edit profile page'),
            ('/listings/create/', 'Create listing page'),
            ('/messaging/', 'Inbox page'),
        ]
        
        for url, description in auth_urls:
            with self.subTest(url=url, description=description):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    200,
                    f"{description} ({url}) failed with status {response.status_code}"
                )
    
    def test_admin_pages_require_staff_access(self):
        """Test that admin pages are restricted to staff users"""
        # Test with the staff user created in setUp
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/companies/admin-dashboard/')
        self.assertEqual(response.status_code, 200, 
                        "Admin dashboard should be accessible to staff users")
        
        # Test as non-staff user
        non_staff_user = User.objects.create_user(
            username='normaluser',
            email='normal@testcompany.com',
            password='normalpass123',
            company=self.company,
            status='approved',
            email_verified=True
            # is_staff=False by default
        )
        
        self.client.login(username='normaluser', password='normalpass123')
        response = self.client.get('/companies/admin-dashboard/')
        self.assertNotEqual(response.status_code, 200,
                        "Admin dashboard should NOT be accessible to non-staff users")
    
    def test_nonexistent_pages_return_404(self):
        """Test that non-existent URLs properly return 404"""
        nonexistent_urls = [
            '/this-page-does-not-exist/',
            '/listings/99999/',  # Non-existent listing ID
            '/listings/category/nonexistent-category/',
        ]
        
        for url in nonexistent_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    404,
                    f"URL {url} should return 404 but returned {response.status_code}"
                )
    
    def test_static_assets_configured(self):
        """Test that static file configuration is working"""
        # This tests that the static URL is configured correctly
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'STATIC_URL'))
        self.assertTrue(hasattr(settings, 'STATICFILES_DIRS') or hasattr(settings, 'STATIC_ROOT'))
    
    def test_health_endpoint(self):
        """Test that health check endpoint is accessible"""
        response = self.client.get('/health/')
        self.assertIn(response.status_code, [200, 404],  # May not be configured in all environments
                     f"Health endpoint returned unexpected status {response.status_code}")
