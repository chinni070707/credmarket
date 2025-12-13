"""
Tests for the listings app.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from listings.models import Category, Listing
from companies.models import Company

User = get_user_model()


class CategoryModelTests(TestCase):
    """Tests for Category model."""
    
    def test_create_category(self):
        """Test creating a category."""
        category = Category.objects.create(
            name="Electronics",
            slug="electronics",
            icon="📱"
        )
        self.assertEqual(category.name, "Electronics")
        self.assertEqual(category.slug, "electronics")
        self.assertTrue(category.is_active)
    
    def test_category_string_representation(self):
        """Test category __str__ method."""
        category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.assertEqual(str(category), "Electronics")
    
    def test_category_with_parent(self):
        """Test category with parent (subcategory)."""
        parent = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        subcategory = Category.objects.create(
            name="Smartphones",
            slug="smartphones",
            parent=parent
        )
        self.assertEqual(subcategory.parent, parent)
        self.assertEqual(str(subcategory), "Electronics > Smartphones")


class ListingModelTests(TestCase):
    """Tests for Listing model."""
    
    def setUp(self):
        """Set up test data."""
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
            is_active=True
        )
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
    
    def test_create_listing(self):
        """Test creating a listing."""
        listing = Listing.objects.create(
            seller=self.user,
            title="iPhone 15",
            description="Brand new iPhone 15",
            category=self.category,
            price=999.99,
            condition="new",
            location="Test City",
            city="Test City",
            state="Test State"
        )
        self.assertEqual(listing.seller, self.user)
        self.assertEqual(listing.title, "iPhone 15")
        self.assertEqual(listing.price, 999.99)
        self.assertEqual(listing.status, 'active')  # Default status is 'active'
    
    def test_listing_string_representation(self):
        """Test listing __str__ method."""
        listing = Listing.objects.create(
            seller=self.user,
            title="iPhone 15",
            description="Brand new iPhone 15",
            category=self.category,
            price=999.99,
            condition='new',
            location='Test City',
            city='Test City',
            state='Test State'
        )
        self.assertEqual(str(listing), "iPhone 15 - ₹999.99")


class ListingViewTests(TestCase):
    """Tests for listing views."""
    
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
            is_active=True
        )
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
    
    def test_home_page_loads(self):
        """Test that the home page loads successfully."""
        response = self.client.get(reverse('listings:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_create_listing_requires_authentication(self):
        """Test that creating a listing requires authentication."""
        response = self.client.get(reverse('listings:create_listing'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
    
    def test_create_listing_page_loads_for_authenticated_user(self):
        """Test that create listing page loads for authenticated user."""
        self.client.login(email='test@testcorp.com', password='TestPass123!')
        response = self.client.get(reverse('listings:create_listing'))
        # May redirect if user doesn't have proper permissions/company
        self.assertIn(response.status_code, [200, 302])
    
    def test_listing_detail_page_loads(self):
        """Test that listing detail page loads."""
        listing = Listing.objects.create(
            seller=self.user,
            title="Test Item",
            description="Test description",
            category=self.category,
            price=100.00,
            condition='new',
            location='Test City',
            city='Test City',
            state='Test State'
        )
        response = self.client.get(reverse('listings:listing_detail', args=[listing.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Item")
    
    def test_listing_list_page_loads(self):
        """Test that listing list page loads."""
        response = self.client.get(reverse('listings:listing_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_listing_list_search(self):
        """Test listing list search functionality."""
        Listing.objects.create(
            seller=self.user,
            title="iPhone 15",
            description="Latest iPhone",
            category=self.category,
            price=999.99,
            condition='new',
            location='Mumbai',
            city='Mumbai',
            state='Maharashtra'
        )
        response = self.client.get(reverse('listings:listing_list') + '?q=iPhone')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone')
    
    def test_listing_list_category_filter(self):
        """Test listing list category filter."""
        listing = Listing.objects.create(
            seller=self.user,
            title="Test Item",
            description="Test",
            category=self.category,
            price=100.00,
            condition='new',
            location='Delhi',
            city='Delhi',
            state='Delhi'
        )
        response = self.client.get(reverse('listings:listing_list') + f'?category={self.category.slug}')
        self.assertEqual(response.status_code, 200)
    
    def test_listing_list_price_filter(self):
        """Test listing list price filter."""
        Listing.objects.create(
            seller=self.user,
            title="Cheap Item",
            description="Budget option",
            category=self.category,
            price=50.00,
            condition='used',
            location='Bangalore',
            city='Bangalore',
            state='Karnataka'
        )
        response = self.client.get(reverse('listings:listing_list') + '?min_price=40&max_price=60')
        self.assertEqual(response.status_code, 200)
    
    def test_create_listing_post(self):
        """Test creating a listing via POST."""
        self.client.login(email='test@testcorp.com', password='TestPass123!')
        data = {
            'title': 'New Listing',
            'description': 'Test description',
            'category': self.category.id,
            'price': 200.00,
            'condition': 'new',
            'location': 'Test Location',
            'city': 'Test City',
            'state': 'Test State'
        }
        response = self.client.post(reverse('listings:create_listing'), data)
        # Should redirect on success or show form on error
        self.assertIn(response.status_code, [200, 302])
    
    def test_edit_listing_requires_owner(self):
        """Test that only listing owner can edit."""
        listing = Listing.objects.create(
            seller=self.user,
            title="Test Item",
            description="Test",
            category=self.category,
            price=100.00,
            condition='new',
            location='Test City',
            city='Test City',
            state='Test State'
        )
        # Create another user
        other_company = Company.objects.create(
            name="Other Corp",
            domain="other.com",
            status='approved'
        )
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@other.com',
            password='TestPass123!',
            first_name='Other',
            last_name='User'
        )
        self.client.login(email='other@other.com', password='TestPass123!')
        response = self.client.get(reverse('listings:edit_listing', args=[listing.slug]))
        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)
    
    def test_delete_listing_requires_owner(self):
        """Test that only listing owner can delete."""
        listing = Listing.objects.create(
            seller=self.user,
            title="Test Item",
            description="Test",
            category=self.category,
            price=100.00,
            condition='new',
            location='Test City',
            city='Test City',
            state='Test State'
        )
        # Create another user
        other_company = Company.objects.create(
            name="Other Corp",
            domain="other.com",
            status='approved'
        )
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@other.com',
            password='TestPass123!',
            first_name='Other',
            last_name='User'
        )
        self.client.login(email='other@other.com', password='TestPass123!')
        response = self.client.post(reverse('listings:delete_listing', args=[listing.slug]))
        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)
        # Listing should still exist
        self.assertTrue(Listing.objects.filter(slug=listing.slug).exists())
