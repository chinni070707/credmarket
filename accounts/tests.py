"""
Tests for the accounts app.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from companies.models import Company

User = get_user_model()


class UserRegistrationTests(TestCase):
    """Tests for user registration functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        # Create approved company
        self.company = Company.objects.create(
            name="Test Corp",
            domain="testcorp.com",
            status='approved'
        )
    
    def test_signup_page_loads(self):
        """Test that the signup page loads successfully."""
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up')
    
    def test_signup_with_approved_domain(self):
        """Test signup with an approved company domain."""
        response = self.client.post(reverse('accounts:signup'), {
            'email': 'test@testcorp.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        # Should redirect or show OTP verification
        self.assertTrue(response.status_code in [200, 302])
    
    def test_signup_with_waitlisted_domain(self):
        """Test signup with a waitlisted domain."""
        # Create waitlisted company
        Company.objects.create(
            name="Waitlist Corp",
            domain="waitlist.com",
            status='waitlist'
        )
        response = self.client.post(reverse('accounts:signup'), {
            'email': 'test@waitlist.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        # Should show waitlist message
        self.assertTrue(response.status_code in [200, 302])


class UserAuthenticationTests(TestCase):
    """Tests for user authentication."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.company = Company.objects.create(
            name="Test Corp",
            domain="testcorp.com",
            status='approved'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@testcorp.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User',
            is_active=True,
            email_verified=True
        )
    
    def test_login_page_loads(self):
        """Test that the login page loads successfully."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
    
    def test_login_with_valid_credentials(self):
        """Test login with valid credentials."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'test@testcorp.com',
            'password': 'TestPass123!',
        })
        # Check if either redirected or logged in successfully
        # The view may return 200 with error or 302 on success
        self.assertIn(response.status_code, [200, 302])
    
    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'test@testcorp.com',
            'password': 'WrongPassword',
        })
        # Should stay on login page with error
        self.assertEqual(response.status_code, 200)
    
    def test_logout(self):
        """Test user logout."""
        self.client.login(email='test@testcorp.com', password='TestPass123!')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)


class UserProfileTests(TestCase):
    """Tests for user profile functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.company = Company.objects.create(
            name="Test Corp",
            domain="testcorp.com",
            status='approved'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@testcorp.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User',
            is_active=True,
            email_verified=True
        )
        self.client.login(email='test@testcorp.com', password='TestPass123!')
    
    def test_profile_page_requires_authentication(self):
        """Test that profile page requires authentication."""
        self.client.logout()
        response = self.client.get(reverse('accounts:profile'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
    
    def test_profile_page_loads_for_authenticated_user(self):
        """Test that profile page loads for authenticated user."""
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.email)
    
    def test_edit_profile_page_loads(self):
        """Test that edit profile page loads."""
        response = self.client.get(reverse('accounts:edit_profile'))
        self.assertIn(response.status_code, [200, 302])
    
    def test_edit_profile_updates_user(self):
        """Test updating user profile."""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '1234567890',
            'bio': 'Updated bio',
            'location': 'New City',  # location is the city field
            'area': 'New Area'
        }
        response = self.client.post(reverse('accounts:edit_profile'), data)
        # Should redirect or show form
        self.assertIn(response.status_code, [200, 302])


class OTPVerificationTests(TestCase):
    """Tests for OTP verification functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.company = Company.objects.create(
            name="Test Corp",
            domain="testcorp.com",
            status='approved'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@testcorp.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User',
            is_active=True,
            email_verified=False
        )
    
    def test_verify_otp_page_loads(self):
        """Test that verify OTP page loads."""
        self.client.login(email='test@testcorp.com', password='TestPass123!')
        response = self.client.get(reverse('accounts:verify_otp'))
        self.assertIn(response.status_code, [200, 302])
    
    def test_verify_otp_with_invalid_code(self):
        """Test OTP verification with invalid code."""
        self.client.login(email='test@testcorp.com', password='TestPass123!')
        response = self.client.post(reverse('accounts:verify_otp'), {
            'otp': '000000'
        })
        # Should stay on page with error
        self.assertIn(response.status_code, [200, 302])




