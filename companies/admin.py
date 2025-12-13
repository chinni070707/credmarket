from django.contrib import admin
from django.utils import timezone
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'status', 'employee_count', 'created_at', 'approved_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'domain']
    readonly_fields = ['created_at', 'updated_at', 'approved_at', 'employee_count']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Company Information', {
            'fields': ('name', 'domain', 'description', 'website', 'logo')
        }),
        ('Status', {
            'fields': ('status', 'added_by', 'approved_by', 'approved_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'employee_count'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_companies', 'reject_companies', 'move_to_waitlist']
    
    def approve_companies(self, request, queryset):
        """Approve selected companies"""
        for company in queryset:
            company.status = 'approved'
            company.approved_by = request.user
            company.approved_at = timezone.now()
            company.save()
            
            # Update all employees of this company
            company.employees.filter(status='waitlist').update(status='approved')
        
        self.message_user(request, f"{queryset.count()} companies approved successfully.")
    approve_companies.short_description = "Approve selected companies"
    
    def reject_companies(self, request, queryset):
        """Reject selected companies"""
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} companies rejected.")
    reject_companies.short_description = "Reject selected companies"
    
    def move_to_waitlist(self, request, queryset):
        """Move selected companies to waitlist"""
        queryset.update(status='waitlist', approved_at=None, approved_by=None)
        self.message_user(request, f"{queryset.count()} companies moved to waitlist.")
    move_to_waitlist.short_description = "Move to waitlist"
    
    def save_model(self, request, obj, form, change):
        """Auto-set approved_by and approved_at when status changes to approved"""
        if obj.status == 'approved' and not obj.approved_by:
            obj.approved_by = request.user
            obj.approved_at = timezone.now()
        
        if not change:  # New object
            obj.added_by = request.user
        
        super().save_model(request, obj, form, change)
