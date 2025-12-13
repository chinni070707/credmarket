"""
Tests for credmarket app views (error handlers)
"""
import pytest
from django.test import Client
from django.urls import reverse


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
