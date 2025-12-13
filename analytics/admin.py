from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta
from .models import UserActivity, PlatformMetrics
from accounts.models import User
from listings.models import Listing
from messaging.models import Message


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_start', 'session_end', 'page_views', 'duration_minutes']
    list_filter = ['session_start']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['session_start', 'session_end', 'page_views', 'actions_performed']
    date_hierarchy = 'session_start'


@admin.register(PlatformMetrics)
class PlatformMetricsAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'daily_active_users', 'new_signups', 'new_listings', 
        'messages_sent', 'average_session_duration'
    ]
    list_filter = ['date']
    readonly_fields = [
        'date', 'daily_active_users', 'new_signups', 'total_users',
        'new_listings', 'total_active_listings', 'listings_sold',
        'average_listings_per_user', 'messages_sent', 'new_conversations',
        'total_page_views', 'average_session_duration'
    ]
    date_hierarchy = 'date'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='analytics_dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Custom dashboard view with real-time metrics"""
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        last_7_days = today - timedelta(days=7)
        last_30_days = today - timedelta(days=30)
        
        # Daily Active Users (today)
        dau_today = UserActivity.objects.filter(
            session_start__date=today
        ).values('user').distinct().count()
        
        # Daily Active Users (yesterday) for comparison
        dau_yesterday = UserActivity.objects.filter(
            session_start__date=yesterday
        ).values('user').distinct().count()
        
        # Listings per user
        total_users = User.objects.filter(status='approved').count()
        total_listings = Listing.objects.filter(status='active').count()
        listings_per_user = round(total_listings / total_users, 2) if total_users > 0 else 0
        
        # Messages sent today
        messages_today = Message.objects.filter(
            created_at__date=today
        ).count()
        
        # Messages sent yesterday for comparison
        messages_yesterday = Message.objects.filter(
            created_at__date=yesterday
        ).count()
        
        # Average session duration (today)
        avg_duration_today = UserActivity.objects.filter(
            session_start__date=today,
            session_end__isnull=False
        ).aggregate(
            avg_duration=Avg('session_end') - Avg('session_start')
        )
        
        # Calculate average in minutes
        if avg_duration_today['avg_duration']:
            avg_session_minutes = avg_duration_today['avg_duration'].total_seconds() / 60
        else:
            avg_session_minutes = 0
        
        # Weekly metrics
        weekly_users = UserActivity.objects.filter(
            session_start__date__gte=last_7_days
        ).values('user').distinct().count()
        
        weekly_listings = Listing.objects.filter(
            created_at__date__gte=last_7_days
        ).count()
        
        weekly_messages = Message.objects.filter(
            created_at__date__gte=last_7_days
        ).count()
        
        # Monthly metrics
        monthly_users = UserActivity.objects.filter(
            session_start__date__gte=last_30_days
        ).values('user').distinct().count()
        
        monthly_listings = Listing.objects.filter(
            created_at__date__gte=last_30_days
        ).count()
        
        monthly_messages = Message.objects.filter(
            created_at__date__gte=last_30_days
        ).count()
        
        # Top categories
        top_categories = Listing.objects.filter(
            status='active'
        ).values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Most active users (by messages)
        most_active_users = User.objects.annotate(
            message_count=Count('sent_messages')
        ).order_by('-message_count')[:10]
        
        # Recent metrics (last 7 days)
        recent_metrics = PlatformMetrics.objects.filter(
            date__gte=last_7_days
        ).order_by('-date')
        
        context = {
            'title': 'Analytics Dashboard',
            'today': today,
            
            # Today's metrics
            'dau_today': dau_today,
            'dau_yesterday': dau_yesterday,
            'dau_change': dau_today - dau_yesterday,
            'listings_per_user': listings_per_user,
            'messages_today': messages_today,
            'messages_yesterday': messages_yesterday,
            'messages_change': messages_today - messages_yesterday,
            'avg_session_minutes': round(avg_session_minutes, 2),
            
            # Weekly metrics
            'weekly_users': weekly_users,
            'weekly_listings': weekly_listings,
            'weekly_messages': weekly_messages,
            
            # Monthly metrics
            'monthly_users': monthly_users,
            'monthly_listings': monthly_listings,
            'monthly_messages': monthly_messages,
            
            # Overall stats
            'total_users': total_users,
            'total_listings': total_listings,
            
            # Top data
            'top_categories': top_categories,
            'most_active_users': most_active_users,
            'recent_metrics': recent_metrics,
        }
        
        return render(request, 'admin/analytics_dashboard.html', context)
