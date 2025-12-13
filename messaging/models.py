from django.db import models
from django.db.models import Q


class Conversation(models.Model):
    """
    Conversation between buyer and seller about a listing
    """
    listing = models.ForeignKey(
        'listings.Listing',
        on_delete=models.CASCADE,
        related_name='conversations'
    )
    buyer = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='buyer_conversations'
    )
    seller = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='seller_conversations'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        ordering = ['-updated_at']
        unique_together = ['listing', 'buyer']
    
    def __str__(self):
        return f"Conv: {self.buyer.email} & {self.seller.email} about {self.listing.title}"
    
    def get_last_message(self):
        """Get the last message in conversation"""
        return self.messages.last()
    
    def get_other_user(self, current_user):
        """Get the other participant in conversation"""
        return self.seller if current_user == self.buyer else self.buyer
    
    def unread_count(self, user):
        """Count unread messages for a user"""
        return self.messages.filter(sender__ne=user, is_read=False).count()


class Message(models.Model):
    """
    Individual messages in a conversation
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.email} to {self.receiver.email}: {self.content[:50]}"
    
    def mark_as_read(self):
        """Mark message as read"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
