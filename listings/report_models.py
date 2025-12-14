from django.db import models
from django.conf import settings
from .models import Listing


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
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_reports')
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(help_text='Please provide details about this report')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Admin fields
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
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
