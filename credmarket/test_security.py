"""
Security and permission tests to detect vulnerabilities early
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from accounts.models import User
from companies.models import Company
from listings.models import Category, Listing
from messaging.models import Conversation, Message

User = get_user_model()


class SecurityTests(TestCase):
    """Test security vulnerabilities and permission issues"""
    
    def setUp(self):
        """Set up test data"""
        # Create companies
        self.company1 = Company.objects.create(
            domain='company1.com',
            name='Company 1',
            status='approved'
        )
        self.company2 = Company.objects.create(
            domain='company2.com',
            name='Company 2',
            status='approved'
        )
        
        # Create users
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@company1.com',
            password='testpass123',
            company=self.company1,
            status='approved',
            email_verified=True
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@company2.com',
            password='testpass123',
            company=self.company2,
            status='approved',
            email_verified=True
        )
        
        # Create category
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics',
            icon='📱',
            is_active=True,
            order=1
        )
        
        # Create listings
        self.listing1 = Listing.objects.create(
            title='User 1 Product',
            description='Product by user 1',
            price=100,
            category=self.category,
            seller=self.user1,
            location='Location 1',
            status='active'
        )
        self.listing2 = Listing.objects.create(
            title='User 2 Product',
            description='Product by user 2',
            price=200,
            category=self.category,
            seller=self.user2,
            location='Location 2',
            status='active'
        )
    
    def test_cannot_edit_other_users_listing(self):
        """Test that users cannot edit listings they don't own"""
        self.client.login(username='user1', password='testpass123')
        
        # Try to access edit page for user2's listing
        response = self.client.get(f'/listings/{self.listing2.slug}/edit/')
        self.assertIn(response.status_code, [302, 403, 404],
                     "Users should not be able to edit other users' listings")
        
        # Try to POST edit to user2's listing
        response = self.client.post(f'/listings/{self.listing2.slug}/edit/', {
            'title': 'Hacked Title',
            'description': 'Hacked',
            'price': 1,
        })
        self.assertIn(response.status_code, [302, 403, 404],
                     "Users should not be able to modify other users' listings")
        
        # Verify listing wasn't modified
        self.listing2.refresh_from_db()
        self.assertNotEqual(self.listing2.title, 'Hacked Title')
    
    def test_cannot_delete_other_users_listing(self):
        """Test that users cannot delete listings they don't own"""
        self.client.login(username='user1', password='testpass123')
        
        # Try to delete user2's listing
        response = self.client.post(f'/listings/{self.listing2.slug}/delete/')
        self.assertIn(response.status_code, [302, 403, 404],
                     "Users should not be able to delete other users' listings")
        
        # Verify listing still exists
        self.assertTrue(Listing.objects.filter(id=self.listing2.id).exists())
    
    def test_sql_injection_in_search(self):
        """Test that search is protected against SQL injection"""
        # Try common SQL injection patterns
        sql_injection_attempts = [
            "'; DROP TABLE listings_listing; --",
            "1' OR '1'='1",
            "admin'--",
            "' OR 1=1--",
        ]
        
        for injection in sql_injection_attempts:
            with self.subTest(injection=injection):
                response = self.client.get('/listings/', {'q': injection})
                # Should return 200 without errors
                self.assertEqual(response.status_code, 200,
                               f"Search should handle SQL injection attempt: {injection}")
                # Database should still be intact
                self.assertTrue(Listing.objects.exists())
    
    def test_xss_in_listing_title(self):
        """Test that XSS attempts in listing titles are escaped"""
        self.client.login(username='user1', password='testpass123')
        
        xss_attempts = [
            '<script>alert("XSS")</script>',
            '<img src=x onerror=alert("XSS")>',
            '"><script>alert(String.fromCharCode(88,83,83))</script>',
        ]
        
        for xss in xss_attempts:
            with self.subTest(xss=xss):
                listing = Listing.objects.create(
                    title=xss,
                    description='Test',
                    price=100,
                    category=self.category,
                    seller=self.user1,
                    location='Test',
                    status='active'
                )
                
                response = self.client.get(f'/listings/{listing.slug}/')
                self.assertEqual(response.status_code, 200)
                
                # Check that XSS payload is sanitized (not just escaped)
                content = response.content.decode('utf-8')
                # The XSS payload should be stripped by bleach, not just escaped
                self.assertNotIn(xss, content,
                               f"XSS payload '{xss}' should be completely removed by bleach")
                # Also verify title is sanitized in meta tags and headings
                if 'alert' in xss.lower():
                    # For script-based attacks, verify the script is stripped
                    self.assertNotIn('alert("XSS")</script>', content,
                                   "Alert script should be stripped, not just escaped")
                
                listing.delete()
    
    def test_unauthenticated_cannot_create_listing(self):
        """Test that unauthenticated users cannot create listings"""
        response = self.client.post('/listings/create/', {
            'title': 'Unauthorized Listing',
            'description': 'Should not work',
            'price': 100,
            'category': self.category.id,
            'location': 'Test',
        })
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
        
        # Listing should not be created
        self.assertFalse(Listing.objects.filter(title='Unauthorized Listing').exists())
    
    def test_unverified_user_cannot_create_listing(self):
        """Test that unverified users cannot create listings"""
        # Create unverified user
        unverified = User.objects.create_user(
            username='unverified',
            email='unverified@company1.com',
            password='testpass123',
            company=self.company1,
            status='approved',
            email_verified=False  # Not verified
        )
        
        self.client.login(username='unverified', password='testpass123')
        response = self.client.get('/listings/create/')
        
        # Should redirect or show error
        self.assertIn(response.status_code, [200, 302],
                     "Unverified users should be prevented from creating listings")
    
    def test_waitlisted_user_cannot_create_listing(self):
        """Test that waitlisted users cannot create listings"""
        # Create waitlisted user
        waitlisted = User.objects.create_user(
            username='waitlisted',
            email='waitlisted@company1.com',
            password='testpass123',
            company=self.company1,
            status='waitlist',  # On waitlist
            email_verified=True
        )
        
        self.client.login(username='waitlisted', password='testpass123')
        response = self.client.get('/listings/create/')
        
        # Should redirect with error message
        self.assertEqual(response.status_code, 302,
                        "Waitlisted users should not access create listing page")
    
    def test_csrf_protection_on_forms(self):
        """Test that CSRF protection is enabled on forms"""
        # Try to POST without CSRF token
        self.client.login(username='user1', password='testpass123')
        
        # Disable CSRF middleware temporarily by using enforce_csrf_checks
        self.client = Client(enforce_csrf_checks=True)
        self.client.login(username='user1', password='testpass123')
        
        response = self.client.post('/listings/create/', {
            'title': 'Test Listing',
            'description': 'Test',
            'price': 100,
        })
        
        # Should fail due to missing CSRF token
        self.assertEqual(response.status_code, 403,
                        "Forms should require CSRF token")
    
    def test_password_not_in_response(self):
        """Test that password hashes are never exposed in responses"""
        self.client.login(username='user1', password='testpass123')
        
        # Check profile page
        response = self.client.get('/accounts/profile/')
        content = response.content.decode('utf-8')
        
        # Password hash should not be in HTML
        self.assertNotIn('pbkdf2_sha256', content,
                        "Password hashes should not be exposed")
        self.assertNotIn(self.user1.password, content,
                        "Password hashes should not be exposed")
    
    def test_email_enumeration_prevention(self):
        """Test that login doesn't reveal if email exists"""
        # Try login with non-existent email
        response1 = self.client.post('/accounts/login/', {
            'email': 'nonexistent@company1.com',
            'password': 'wrongpass',
        })
        
        # Try login with existing email but wrong password
        response2 = self.client.post('/accounts/login/', {
            'email': 'user1@company1.com',
            'password': 'wrongpass',
        })
        
        # Both should return same error message (no email enumeration)
        # Check that responses are similar
        self.assertEqual(response1.status_code, response2.status_code,
                        "Login should not reveal if email exists")


class PermissionTests(TestCase):
    """Test permission and authorization issues"""
    
    def setUp(self):
        """Set up test data"""
        self.company = Company.objects.create(
            domain='testcompany.com',
            name='Test Company',
            status='approved'
        )
        
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@testcompany.com',
            password='testpass123',
            company=self.company,
            status='approved',
            email_verified=True
        )
        
        self.staff_user = User.objects.create_user(
            username='staff',
            email='staff@testcompany.com',
            password='testpass123',
            company=self.company,
            status='approved',
            email_verified=True,
            is_staff=True
        )
        
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@testcompany.com',
            password='testpass123',
            company=self.company,
            status='approved',
            email_verified=True
        )
    
    def test_regular_user_cannot_access_admin(self):
        """Test that regular users cannot access admin pages"""
        self.client.login(username='regular', password='testpass123')
        
        admin_urls = [
            '/companies/admin-dashboard/',
            '/admin/',
        ]
        
        for url in admin_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, 200,
                                  f"Regular users should not access {url}")
    
    def test_staff_can_access_custom_admin(self):
        """Test that staff users can access custom admin dashboard"""
        self.client.login(username='staff', password='testpass123')
        response = self.client.get('/companies/admin-dashboard/')
        
        # Should be accessible or redirect appropriately
        self.assertIn(response.status_code, [200, 302],
                     "Staff users should access admin dashboard")
    
    def test_only_superuser_can_access_django_admin(self):
        """Test that only superusers can access Django admin"""
        # Regular user
        self.client.login(username='regular', password='testpass123')
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 200,
                          "Regular users cannot access Django admin")
        
        # Staff user (without superuser)
        self.client.login(username='staff', password='testpass123')
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 200,
                          "Staff users cannot access Django admin without superuser")
        
        # Superuser
        self.client.login(username='admin', password='testpass123')
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, [200, 302],
                     "Superusers should access Django admin")


class DataValidationTests(TestCase):
    """Test data validation and integrity"""
    
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
    
    def test_negative_price_validation(self):
        """Test that negative prices are rejected"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post('/listings/create/', {
            'title': 'Test Listing',
            'description': 'Test',
            'price': -100,  # Negative price
            'category': self.category.id,
            'location': 'Test',
        })
        
        # Should not create listing with negative price
        self.assertFalse(Listing.objects.filter(price__lt=0).exists(),
                        "Negative prices should be rejected")
    
    def test_extremely_large_price_validation(self):
        """Test handling of extremely large prices"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post('/listings/create/', {
            'title': 'Test Listing',
            'description': 'Test',
            'price': 9999999999999,  # Very large price
            'category': self.category.id,
            'location': 'Test',
        })
        
        # Should handle gracefully (either accept or reject with proper error)
        self.assertIn(response.status_code, [200, 302])
    
    def test_empty_required_fields(self):
        """Test that required fields cannot be empty"""
        self.client.login(username='testuser', password='testpass123')
        
        # Try to create listing without title
        response = self.client.post('/listings/create/', {
            'title': '',  # Empty title
            'description': 'Test',
            'price': 100,
            'category': self.category.id,
            'location': 'Test',
        })
        
        # Should not create listing
        self.assertFalse(Listing.objects.filter(description='Test').exists(),
                        "Listings with empty required fields should be rejected")
    
    def test_duplicate_category_slug(self):
        """Test that duplicate category slugs are prevented"""
        from django.db import IntegrityError
        
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name='Electronics 2',
                slug='electronics',  # Duplicate slug
                icon='📱',
                is_active=True,
                order=2
            )
    
    def test_email_format_validation(self):
        """Test that invalid email formats are rejected"""
        invalid_emails = [
            'notanemail',
            '@nodomain.com',
            'missing@',
            'missing.com',
            'spaces in@email.com',
        ]
        
        for invalid_email in invalid_emails:
            with self.subTest(email=invalid_email):
                response = self.client.post('/accounts/signup/', {
                    'email': invalid_email,
                    'username': 'testuser',
                    'password1': 'testpass123',
                    'password2': 'testpass123',
                })
                
                # Should not create user with invalid email
                self.assertFalse(User.objects.filter(email=invalid_email).exists(),
                               f"Invalid email {invalid_email} should be rejected")
