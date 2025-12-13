from django.contrib import admin
from .models import Category, Listing, ListingImage


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


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ['listing', 'caption', 'order', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['listing__title', 'caption']
