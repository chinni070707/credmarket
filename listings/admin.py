from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Listing, ListingImage, ListingReport
import logging

logger = logging.getLogger(__name__)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug', 'listing_count', 'is_active', 'order']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Category Info', {
            'fields': ('name', 'slug', 'parent', 'icon', 'description')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'category', 'price', 'condition', 'status', 'views_count', 'created_at']
    list_filter = ['status', 'condition', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'description', 'seller__email', 'location', 'city']
    readonly_fields = ['views_count', 'created_at', 'updated_at', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    
    inlines = [ListingImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'category', 'seller')
        }),
        ('Pricing & Condition', {
            'fields': ('price', 'is_negotiable', 'condition')
        }),
        ('Location', {
            'fields': ('location', 'city', 'state', 'pincode')
        }),
        ('Status & Features', {
            'fields': ('status', 'is_featured', 'expires_at')
        }),
        ('Metrics', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_sold', 'mark_as_active', 'feature_listings']
    
    def mark_as_sold(self, request, queryset):
        queryset.update(status='sold')
        self.message_user(request, f"{queryset.count()} listings marked as sold.")
    mark_as_sold.short_description = "Mark as sold"
    
    def mark_as_active(self, request, queryset):
        queryset.update(status='active')
        self.message_user(request, f"{queryset.count()} listings marked as active.")
    mark_as_active.short_description = "Mark as active"
    
    def feature_listings(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} listings featured.")
    feature_listings.short_description = "Feature selected listings"


@admin.register(ListingReport)
class ListingReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'listing_link', 'reporter_email', 'reason_display', 'status_badge', 'report_count', 'created_at', 'action_buttons']
    list_filter = ['status', 'reason', 'created_at']
    search_fields = ['listing__title', 'reporter__email', 'description', 'admin_notes']
    readonly_fields = ['reporter', 'listing', 'reason', 'description', 'created_at', 'updated_at', 'report_count_display']
    
    fieldsets = (
        ('Report Details', {
            'fields': ('listing', 'reporter', 'reason', 'description', 'report_count_display', 'created_at')
        }),
        ('Admin Review', {
            'fields': ('status', 'reviewed_by', 'admin_notes', 'action_taken', 'resolved_at')
        }),
    )
    
    actions = ['mark_as_reviewing', 'mark_as_resolved', 'mark_as_dismissed', 'deactivate_reported_listings']
    
    def listing_link(self, obj):
        """Link to the reported listing"""
        url = reverse('admin:listings_listing_change', args=[obj.listing.id])
        return format_html('<a href="{}" target="_blank">{}</a>', url, obj.listing.title[:50])
    listing_link.short_description = 'Listing'
    
    def reporter_email(self, obj):
        """Display reporter email"""
        return obj.reporter.email
    reporter_email.short_description = 'Reporter'
    
    def reason_display(self, obj):
        """Display reason with color coding"""
        colors = {
            'fraud': '#dc2626',
            'inappropriate': '#ea580c',
            'spam': '#ca8a04',
            'duplicate': '#0891b2',
        }
        color = colors.get(obj.reason, '#6b7280')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_reason_display()
        )
    reason_display.short_description = 'Reason'
    
    def status_badge(self, obj):
        """Display status with badge"""
        colors = {
            'pending': '#eab308',
            'reviewing': '#3b82f6',
            'resolved': '#10b981',
            'dismissed': '#6b7280',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def report_count(self, obj):
        """Total reports for this listing"""
        count = obj.get_report_count()
        if count > 3:
            return format_html('<span style="color: #dc2626; font-weight: bold;">⚠️ {}</span>', count)
        elif count > 1:
            return format_html('<span style="color: #ea580c; font-weight: bold;">{}</span>', count)
        return count
    report_count.short_description = 'Total Reports'
    
    def report_count_display(self, obj):
        """For detail view"""
        return obj.get_report_count()
    report_count_display.short_description = 'Total Reports for this Listing'
    
    def action_buttons(self, obj):
        """Quick action buttons"""
        listing_url = f'/listings/{obj.listing.id}/'
        return format_html(
            '<a href="{}" target="_blank" style="background-color: #3b82f6; color: white; padding: 4px 12px; border-radius: 4px; text-decoration: none; margin-right: 5px;">View Listing</a>',
            listing_url
        )
    action_buttons.short_description = 'Actions'
    
    def mark_as_reviewing(self, request, queryset):
        queryset.update(status='reviewing', reviewed_by=request.user)
        self.message_user(request, f"{queryset.count()} reports marked as under review.")
    mark_as_reviewing.short_description = "Mark as under review"
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved', reviewed_by=request.user, resolved_at=timezone.now())
        self.message_user(request, f"{queryset.count()} reports marked as resolved.")
    mark_as_resolved.short_description = "Mark as resolved"
    
    def mark_as_dismissed(self, request, queryset):
        queryset.update(status='dismissed', reviewed_by=request.user, resolved_at=timezone.now())
        self.message_user(request, f"{queryset.count()} reports dismissed.")
    mark_as_dismissed.short_description = "Dismiss reports"
    
    def deactivate_reported_listings(self, request, queryset):
        """Deactivate all listings in selected reports"""
        listings = [report.listing for report in queryset]
        count = 0
        for listing in listings:
            listing.status = 'inactive'
            listing.save()
            count += 1
        queryset.update(
            status='resolved',
            reviewed_by=request.user,
            action_taken='Listing deactivated',
            resolved_at=timezone.now()
        )
        self.message_user(request, f"{count} listings deactivated and {queryset.count()} reports resolved.")
    deactivate_reported_listings.short_description = "Deactivate reported listings"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('listing', 'reporter', 'reviewed_by')


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ['listing', 'caption', 'order', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['listing__title', 'caption']
