from django.db import models
from django.utils.text import slugify
import json
import bleach


class Category(models.Model):
    """
    Product categories (similar to OLX structure)
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    icon = models.CharField(max_length=50, blank=True, help_text='Font Awesome icon class or emoji')
    image = models.ImageField(upload_to='categories/', blank=True, null=True, help_text='Category image for visual display')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text='Display order')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def listing_count(self):
        """Get number of active listings in this category"""
        return self.listings.filter(status='active').count()


class Listing(models.Model):
    """
    Product listings by users
    """
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('expired', 'Expired'),
        ('deleted', 'Deleted'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'Brand New'),
        ('like_new', 'Like New'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='listings'
    )
    
    # Seller
    seller = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='listings'
    )
    
    # Pricing & Condition
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_negotiable = models.BooleanField(default=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    
    # Location
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10, blank=True)
    
    # Status & Features
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False, help_text='Promoted listing')
    
    # Category-specific attributes (flexible JSON field)
    # Examples:
    # Vehicles: {"fuel_type": "Petrol", "km_driven": "15000", "year": "2020", "brand": "Honda"}
    # Rent: {"furnishing": "Semi-Furnished", "bedrooms": "2", "bathrooms": "2", "deposit": "50000"}
    # Real Estate: {"carpet_area": "1200", "total_floors": "10", "floor_number": "5", "facing": "East"}
    attributes = models.JSONField(
        default=dict, 
        blank=True,
        help_text='Category-specific attributes as key-value pairs'
    )
    
    # Engagement
    views_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['seller', 'status']),  # For user's own listings
            models.Index(fields=['city', 'status']),  # For location-based queries
            models.Index(fields=['is_featured', 'status']),  # For featured listings
        ]
    
    def __str__(self):
        return f"{self.title} - ₹{self.price}"
    
    def save(self, *args, **kwargs):
        # Sanitize user input to prevent XSS attacks
        if self.title:
            self.title = bleach.clean(self.title, tags=[], strip=True)
        if self.description:
            self.description = bleach.clean(self.description, tags=[], strip=True)
        
        if not self.slug:
            import uuid
            self.slug = slugify(self.title) + '-' + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)
    
    def get_primary_image(self):
        """Get the first image as primary"""
        return self.images.first()
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class ListingImage(models.Model):
    """
    Images for listings (multiple images per listing)
    """
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='listings/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Listing Image'
        verbose_name_plural = 'Listing Images'
        ordering = ['order', 'uploaded_at']
    
    def __str__(self):
        return f"Image for {self.listing.title}"


class ListingReport(models.Model):
    """Reports submitted by users for listings"""
    
    REPORT_REASONS = [
        ('spam', 'Spam or Misleading'),
        ('inappropriate', 'Inappropriate Content'),
        ('fraud', 'Suspected Fraud'),
        ('duplicate', 'Duplicate Listing'),
        ('sold', 'Already Sold (Not Removed)'),
        ('wrong_category', 'Wrong Category'),
        ('fake_price', 'Fake or Misleading Price'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='submitted_reports')
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(help_text='Please provide details about this report')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Admin fields
    reviewed_by = models.ForeignKey(
        'accounts.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reviewed_reports'
    )
    admin_notes = models.TextField(blank=True, help_text='Internal notes from admin')
    action_taken = models.CharField(
        max_length=100, 
        blank=True,
        help_text='Action taken by admin (e.g., Listing deactivated, Warning sent, etc.)'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['listing', '-created_at']),
        ]
        # Prevent duplicate reports from same user for same listing
        unique_together = ['listing', 'reporter']
    
    def __str__(self):
        return f"Report by {self.reporter.email} - {self.get_reason_display()} - {self.listing.title[:30]}"
    
    def get_report_count(self):
        """Get total reports for this listing"""
        return ListingReport.objects.filter(listing=self.listing).count()
