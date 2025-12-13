from django.db import models


class Company(models.Model):
    """
    Model for approved/waitlisted companies
    """
    
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('waitlist', 'Waitlist'),
        ('rejected', 'Rejected'),
    ]
    
    name = models.CharField(max_length=200)
    domain = models.CharField(
        max_length=255,
        unique=True,
        help_text='Email domain (e.g., google.com, microsoft.com)'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='waitlist'
    )
    description = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='companies/', blank=True, null=True)
    
    # Admin tracking
    added_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='added_companies'
    )
    approved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_companies'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.domain}) - {self.status}"
    
    def employee_count(self):
        """Get number of registered employees"""
        return self.employees.count()
    
    def is_approved(self):
        """Check if company is approved"""
        return self.status == 'approved'
