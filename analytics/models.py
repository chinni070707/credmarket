from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserActivity(models.Model):
    """
    Track user activity for analytics
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    session_start = models.DateTimeField(auto_now_add=True)
    session_end = models.DateTimeField(null=True, blank=True)
    page_views = models.IntegerField(default=0)
    actions_performed = models.JSONField(default=list, blank=True)
    
    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-session_start']
    
    def __str__(self):
        return f"{self.user.email} - {self.session_start.date()}"
    
    @property
    def duration_minutes(self):
        """Calculate session duration in minutes"""
        if self.session_end:
            delta = self.session_end - self.session_start
            return delta.total_seconds() / 60
        return 0


class PlatformMetrics(models.Model):
    """
    Daily aggregated metrics for the platform
    """
    date = models.DateField(unique=True)
    
    # User metrics
    daily_active_users = models.IntegerField(default=0)
    new_signups = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)
    
    # Listing metrics
    new_listings = models.IntegerField(default=0)
    total_active_listings = models.IntegerField(default=0)
    listings_sold = models.IntegerField(default=0)
    average_listings_per_user = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Messaging metrics
    messages_sent = models.IntegerField(default=0)
    new_conversations = models.IntegerField(default=0)
    
    # Engagement metrics
    total_page_views = models.IntegerField(default=0)
    average_session_duration = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # in minutes
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Platform Metric'
        verbose_name_plural = 'Platform Metrics'
        ordering = ['-date']
    
    def __str__(self):
        return f"Metrics for {self.date}"
