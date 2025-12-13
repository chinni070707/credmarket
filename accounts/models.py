from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator


class User(AbstractUser):
    """
    Custom User model for CredMarket.
    Extends Django's AbstractUser with additional fields.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('waitlist', 'Waitlisted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ]
    
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text='Corporate email address'
    )
    personal_email = models.EmailField(
        validators=[EmailValidator()],
        help_text='Personal email for notifications',
        blank=True,
        default='abcd@hello.com'
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=False, help_text='City name')
    area = models.CharField(max_length=100, blank=True, help_text='Locality/Area within city')
    
    # Geolocation coordinates (optional)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Latitude coordinate')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Longitude coordinate')
    
    # Privacy settings
    display_name = models.CharField(max_length=50, blank=True, help_text='Anonymous username for listings')
    show_real_name = models.BooleanField(default=True, help_text='Show real name in listings')
    
    # Email notification preferences
    notify_new_company_listings = models.BooleanField(default=True, help_text='Email me when new items are listed in my company')
    notify_unread_messages = models.BooleanField(default=True, help_text='Email me about unread messages after 15 minutes')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Make email the primary identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} ({self.get_full_name() or 'No Name'})"
    
    def get_display_name(self):
        """Get the name to display in listings"""
        if self.show_real_name:
            return self.get_full_name()
        elif self.display_name:
            return self.display_name
        else:
            # Generate default anonymous name from email
            return f"User_{self.email.split('@')[0][:5]}"
    
    def get_company_domain(self):
        """Extract domain from email"""
        return self.email.split('@')[1] if '@' in self.email else None
    
    def is_verified(self):
        """Check if user is fully verified and approved"""
        return self.email_verified and self.status == 'approved'
    
    def can_create_listing(self):
        """Check if user can create listings"""
        return self.is_verified() and self.is_active


class OTPVerification(models.Model):
    """
    Model to store OTP verification attempts
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_attempts')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    
    class Meta:
        verbose_name = 'OTP Verification'
        verbose_name_plural = 'OTP Verifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp_code}"
    
    def is_valid(self):
        """Check if OTP is still valid"""
        from django.utils import timezone
        return not self.is_used and self.expires_at > timezone.now()
