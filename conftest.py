"""
Pytest configuration and fixtures for CredMarket tests.
"""
import pytest
from django.contrib.auth import get_user_model
from companies.models import Company

User = get_user_model()


@pytest.fixture
def approved_company(db):
    """Create an approved company."""
    company = Company.objects.create(
        name="Test Corporation",
        domain="testcorp.com",
        status='approved'
    )
    return company


@pytest.fixture
def test_user(db, approved_company):
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='testuser@testcorp.com',
        password='TestPass123!',
        first_name='Test',
        last_name='User',
        is_active=True,
        email_verified=True
    )


@pytest.fixture
def admin_user(db, approved_company):
    """Create an admin user."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@testcorp.com',
        password='AdminPass123!',
        first_name='Admin',
        last_name='User'
    )


@pytest.fixture
def authenticated_client(client, test_user):
    """Return a client with an authenticated test user."""
    client.force_login(test_user)
    return client


@pytest.fixture
def admin_client(client, admin_user):
    """Return a client with an authenticated admin user."""
    client.force_login(admin_user)
    return client


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests."""
    pass
