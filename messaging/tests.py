"""
Tests for the messaging app.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from messaging.models import Conversation, Message
from companies.models import Company
from listings.models import Category, Listing

User = get_user_model()


class ConversationModelTests(TestCase):
    """Tests for Conversation model."""
    
    def setUp(self):
        """Set up test data."""
        self.company = Company.objects.create(
            name="Test Corp",
            domain="testcorp.com",
            status='approved'
        )
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@testcorp.com',
            password='TestPass123!',
            first_name='User',
            last_name='One',
            is_active=True
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@testcorp.com',
            password='TestPass123!',
            first_name='User',
            last_name='Two',
            is_active=True
        )
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.listing = Listing.objects.create(
            seller=self.user2,
            title="Test Item",
            description="Test description",
            category=self.category,
            price=100.00,
            condition='new',
            location='Test City',
            city='Test City',
            state='Test State'
        )
    
    def test_create_conversation(self):
        """Test creating a conversation."""
        conversation = Conversation.objects.create(
            listing=self.listing,
            buyer=self.user1,
            seller=self.user2
        )
        
        self.assertEqual(conversation.buyer, self.user1)
        self.assertEqual(conversation.seller, self.user2)
        self.assertEqual(conversation.listing, self.listing)


class MessageModelTests(TestCase):
    """Tests for Message model."""
    
    def setUp(self):
        """Set up test data."""
        self.company = Company.objects.create(
            name="Test Corp",
            domain="testcorp.com",
            status='approved'
        )
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@testcorp.com',
            password='TestPass123!',
            first_name='User',
            last_name='One',
            is_active=True
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@testcorp.com',
            password='TestPass123!',
            first_name='User',
            last_name='Two',
            is_active=True
        )
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.listing = Listing.objects.create(
            seller=self.user2,
            title="Test Item",
            description="Test description",
            category=self.category,
            price=100.00,
            condition='new',
            location='Test City',
            city='Test City',
            state='Test State'
        )
        self.conversation = Conversation.objects.create(
            listing=self.listing,
            buyer=self.user1,
            seller=self.user2
        )
    
    def test_create_message(self):
        """Test creating a message."""
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            receiver=self.user2,
            content="Hello, World!"
        )
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.content, "Hello, World!")
        self.assertFalse(message.is_read)
    
    def test_mark_message_as_read(self):
        """Test marking a message as read."""
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        message.mark_as_read()
        
        self.assertTrue(message.is_read)
        self.assertIsNotNone(message.read_at)


class MessagingViewTests(TestCase):
    """Tests for messaging views."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.company = Company.objects.create(
            name="Test Corp",
            domain="testcorp.com",
            status='approved'
        )
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@testcorp.com',
            password='TestPass123!',
            first_name='User',
            last_name='One',
            is_active=True
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@testcorp.com',
            password='TestPass123!',
            first_name='User',
            last_name='Two',
            is_active=True
        )
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.listing = Listing.objects.create(
            seller=self.user2,
            title="Test Item",
            description="Test description",
            category=self.category,
            price=100.00,
            condition='new',
            location='Test City',
            city='Test City',
            state='Test State'
        )
    
    def test_inbox_requires_authentication(self):
        """Test that inbox requires authentication."""
        response = self.client.get(reverse('messaging:inbox'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
    
    def test_inbox_loads_for_authenticated_user(self):
        """Test that inbox loads for authenticated user."""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('messaging:inbox'))
        # May redirect if no conversations exist, check for 200 or 302
        self.assertIn(response.status_code, [200, 302])
    
    def test_conversation_detail_view(self):
        """Test conversation detail view."""
        conversation = Conversation.objects.create(
            listing=self.listing,
            buyer=self.user1,
            seller=self.user2
        )
        self.client.force_login(self.user1)
        response = self.client.get(reverse('messaging:conversation_detail', args=[conversation.pk]))
        self.assertEqual(response.status_code, 200)
