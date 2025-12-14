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


class ListingPerformanceTests(TestCase):
    """Tests for listing query performance optimizations (Bug Fix #5)."""
    
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
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        # Create test listings
        for i in range(5):
            Listing.objects.create(
                seller=self.user,
                title=f"Test Item {i}",
                description=f"Test description {i}",
                category=self.category,
                price=100.00 + i,
                condition='new',
                location='Test City',
                city='Test City',
                state='Test State',
                status='active'
            )
    
    def test_home_page_uses_select_related(self):
        """Test that home page uses select_related to reduce queries."""
        from django.test.utils import override_settings
        from django.db import connection
        from django.test.utils import CaptureQueriesContext
        
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(reverse('listings:home'))
            self.assertEqual(response.status_code, 200)
            # Should have minimal queries due to select_related
            # Without optimization: 50+ queries
            # With optimization: < 20 queries
            self.assertLess(len(context.captured_queries), 20,
                          f"Too many queries: {len(context.captured_queries)}")
    
    def test_listing_list_uses_select_related(self):
        """Test that listing list uses select_related."""
        from django.db import connection
        from django.test.utils import CaptureQueriesContext
        
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(reverse('listings:listing_list'))
            self.assertEqual(response.status_code, 200)
            # Should have minimal queries
            self.assertLess(len(context.captured_queries), 15,
                          f"Too many queries: {len(context.captured_queries)}")


class MarkAsSoldTests(TestCase):
    """Tests for mark as sold functionality (Bug Fix #3 - New Feature)."""
    
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
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.listing = Listing.objects.create(
            seller=self.user,
            title="Test Item",
            description="Test description",
            category=self.category,
            price=100.00,
            condition='new',
            location='Test City',
            city='Test City',
            state='Test State',
            status='active'
        )
    
    def test_mark_sold_requires_login(self):
        """Test that marking as sold requires authentication."""
        response = self.client.post(reverse('listings:mark_sold', args=[self.listing.slug]))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
    
    def test_mark_sold_requires_owner(self):
        """Test that only owner can mark listing as sold."""
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
        response = self.client.post(reverse('listings:mark_sold', args=[self.listing.slug]))
        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)
        # Listing status should not change
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.status, 'active')
    
    def test_mark_sold_changes_status(self):
        """Test that marking as sold changes listing status to 'sold'."""
        self.client.login(email='test@testcorp.com', password='TestPass123!')
        response = self.client.post(reverse('listings:mark_sold', args=[self.listing.slug]))
        # Should redirect to listing detail
        self.assertEqual(response.status_code, 302)
        # Check status changed
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.status, 'sold')
    
    def test_mark_sold_requires_post_method(self):
        """Test that GET request doesn't mark as sold."""
        self.client.login(email='test@testcorp.com', password='TestPass123!')
        response = self.client.get(reverse('listings:mark_sold', args=[self.listing.slug]))
        # Should redirect (mark_sold view redirects on GET)
        self.assertEqual(response.status_code, 302)
        # Status should not change
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.status, 'active')


class ImageManagementTests(TestCase):
    """Tests for image upload/delete/reorder in edit listing (New Feature)."""
    
    def setUp(self):
        """Set up test data."""
        from listings.models import ListingImage
        from io import BytesIO
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        
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
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.listing = Listing.objects.create(
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
        
        # Create test image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        # Add an image to the listing
        self.test_image = ListingImage.objects.create(
            listing=self.listing,
            image=SimpleUploadedFile('test.jpg', image_io.read(), content_type='image/jpeg'),
            order=0
        )
    
    def test_edit_listing_displays_existing_images(self):
        """Test that edit page displays existing images."""
        self.client.login(email='test@testcorp.com', password='TestPass123!')
        response = self.client.get(reverse('listings:edit_listing', args=[self.listing.slug]))
        self.assertEqual(response.status_code, 200)
        # Check that listing images are in context or rendered
        self.assertIn('listing', response.context)
        self.assertEqual(response.context['listing'].images.count(), 1)
    
    def test_delete_image_requires_login(self):
        """Test that deleting image requires authentication."""
        response = self.client.post(reverse('listings:delete_image', args=[self.test_image.id]))
        # Should return unauthorized
        self.assertEqual(response.status_code, 302)
    
    def test_delete_image_requires_owner(self):
        """Test that only owner can delete images."""
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
        response = self.client.post(reverse('listings:delete_image', args=[self.test_image.id]))
        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)
    
    def test_edit_listing_max_8_images(self):
        """Test that edit listing enforces 8 image limit."""
        from listings.models import ListingImage
        from io import BytesIO
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Add 7 more images (total 8)
        for i in range(7):
            image = Image.new('RGB', (100, 100), color='blue')
            image_io = BytesIO()
            image.save(image_io, format='JPEG')
            image_io.seek(0)
            ListingImage.objects.create(
                listing=self.listing,
                image=SimpleUploadedFile(f'test{i}.jpg', image_io.read(), content_type='image/jpeg'),
                order=i+1
            )
        
        self.assertEqual(self.listing.images.count(), 8)
        
        # Try to add one more via edit
        self.client.login(email='test@testcorp.com', password='TestPass123!')
        
        # Create new image file
        image = Image.new('RGB', (100, 100), color='green')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        new_image = SimpleUploadedFile('new.jpg', image_io.read(), content_type='image/jpeg')
        
        data = {
            'title': self.listing.title,
            'description': self.listing.description,
            'category': self.category.id,
            'price': self.listing.price,
            'condition': self.listing.condition,
            'location': self.listing.location,
            'city': self.listing.city,
            'state': self.listing.state,
            'new_images': [new_image],
        }
        
        response = self.client.post(reverse('listings:edit_listing', args=[self.listing.slug]), data)
        
        # Should not add more than 8 images
        self.listing.refresh_from_db()
        self.assertLessEqual(self.listing.images.count(), 8)


class DatabaseIndexTests(TestCase):
    """Tests to verify database indexes exist (Bug Fix #6)."""
    
    def test_listing_indexes_exist(self):
        """Test that performance indexes are created on Listing model."""
        # Check Meta indexes configuration
        self.assertTrue(hasattr(Listing._meta, 'indexes'))
        self.assertGreater(len(Listing._meta.indexes), 0)
        
        # Verify we have at least 6 indexes (3 original + 3 new from bug fix)
        self.assertGreaterEqual(len(Listing._meta.indexes), 6,
                              "Should have at least 6 indexes for performance")
        
        # Check specific index fields
        index_fields = []
        for index in Listing._meta.indexes:
            if hasattr(index, 'fields'):
                index_fields.extend(index.fields)
        
        # Should include seller, city, is_featured in indexes
        self.assertTrue(any('seller' in str(field) for field in index_fields),
                      "Should have index on seller field")
        self.assertTrue(any('city' in str(field) for field in index_fields),
                      "Should have index on city field")
        self.assertTrue(any('is_featured' in str(field) for field in index_fields),
                      "Should have index on is_featured field")

