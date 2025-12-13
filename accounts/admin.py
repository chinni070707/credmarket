from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTPVerification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'company', 'status', 'email_verified', 'date_joined']
    list_filter = ['status', 'email_verified', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'bio', 'location', 'profile_picture')}),
        ('Company & Verification', {'fields': ('company', 'status', 'email_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    actions = ['approve_users', 'waitlist_users', 'suspend_users']
    
    def approve_users(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} users approved successfully.")
    approve_users.short_description = "Approve selected users"
    
    def waitlist_users(self, request, queryset):
        queryset.update(status='waitlist')
        self.message_user(request, f"{queryset.count()} users moved to waitlist.")
    waitlist_users.short_description = "Move selected users to waitlist"
    
    def suspend_users(self, request, queryset):
        queryset.update(status='suspended', is_active=False)
        self.message_user(request, f"{queryset.count()} users suspended.")
    suspend_users.short_description = "Suspend selected users"


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'otp_code']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
