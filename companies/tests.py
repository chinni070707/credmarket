"""
Tests for the companies app.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from companies.models import Company

User = get_user_model()


class CompanyModelTests(TestCase):
    """Tests for Company model."""
    
    def test_create_company(self):
        """Test creating a company."""
        company = Company.objects.create(
            name="Test Company",
            domain="testcompany.com",
            status='approved'
        )
        self.assertEqual(company.name, "Test Company")
        self.assertEqual(company.domain, "testcompany.com")
        self.assertTrue(company.is_approved())
    
    def test_company_string_representation(self):
        """Test company __str__ method."""
        company = Company.objects.create(
            name="Test Company",
            domain="testcompany.com",
            status='approved'
        )
        self.assertEqual(str(company), "Test Company (testcompany.com) - approved")


class CompanyStatusTests(TestCase):
    """Tests for Company status functionality."""
    
    def test_company_statuses(self):
        """Test different company statuses."""
        approved = Company.objects.create(
            name="Approved Company",
            domain="approved.com",
            status='approved'
        )
        waitlist = Company.objects.create(
            name="Waitlist Company",
            domain="waitlist.com",
            status='waitlist'
        )
        rejected = Company.objects.create(
            name="Rejected Company",
            domain="rejected.com",
            status='rejected'
        )
        
        self.assertTrue(approved.is_approved())
        self.assertFalse(waitlist.is_approved())
        self.assertFalse(rejected.is_approved())
    
    def test_unique_domain(self):
        """Test that company domains must be unique."""
        Company.objects.create(
            name="First Company",
            domain="unique.com",
            status='approved'
        )
        # Trying to create duplicate domain should fail
        with self.assertRaises(Exception):
            Company.objects.create(
                name="Second Company",
                domain="unique.com",
                status='approved'
            )


class AdminDashboardTests(TestCase):
    """Tests for admin dashboard functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@testcorp.com',
            password='AdminPass123!',
            first_name='Admin',
            last_name='User'
        )
        self.company = Company.objects.create(
            name="Test Corp",
            domain="testcorp.com",
            status='approved'
        )
    
    def test_admin_dashboard_requires_superuser(self):
        """Test that admin dashboard requires superuser privileges."""
        # Create regular user
        regular_user = User.objects.create_user(
            username='user',
            email='user@testcorp.com',
            password='UserPass123!',
            first_name='Regular',
            last_name='User',
            is_active=True
        )
        self.client.login(email='user@testcorp.com', password='UserPass123!')
        response = self.client.get(reverse('companies:admin_dashboard'))
        # Should redirect or show 403
        self.assertIn(response.status_code, [302, 403])
    
    def test_admin_dashboard_loads_for_superuser(self):
        """Test that admin dashboard loads for superuser."""
        self.client.login(email='admin@testcorp.com', password='AdminPass123!')
        response = self.client.get(reverse('companies:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_approve_company_action(self):
        """Test approving a waitlisted company."""
        waitlist_company = Company.objects.create(
            name="Waitlist Corp",
            domain="waitlist.com",
            status='waitlist'
        )
        self.client.login(email='admin@testcorp.com', password='AdminPass123!')
        response = self.client.post(
            reverse('companies:approve_company', args=[waitlist_company.id])
        )
        # Should redirect or show success
        self.assertIn(response.status_code, [200, 302])
    
    def test_reject_company_action(self):
        """Test rejecting a waitlisted company."""
        waitlist_company = Company.objects.create(
            name="Waitlist Corp",
            domain="waitlist.com",
            status='waitlist'
        )
        self.client.login(email='admin@testcorp.com', password='AdminPass123!')
        response = self.client.post(
            reverse('companies:reject_company', args=[waitlist_company.id])
        )
        # Should redirect or show success
        self.assertIn(response.status_code, [200, 302])
    


