from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'listing', 'buyer', 'seller', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['listing__title', 'buyer__email', 'seller__email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'sender', 'receiver', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__email', 'receiver__email', 'content']
    readonly_fields = ['created_at', 'read_at']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        # Prevent adding messages from admin
        return False
