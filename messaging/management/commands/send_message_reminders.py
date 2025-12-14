"""
Management command to send email reminders for unread messages
Run this with a cron job every 15 minutes:
*/15 * * * * cd /path/to/credmarket && python manage.py send_message_reminders
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from messaging.models import Message
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send email reminders for messages unread after 15 minutes'

    def handle(self, *args, **options):
        # Find messages that are:
        # 1. Unread (is_read=False)
        # 2. Created more than 15 minutes ago
        # 3. Email reminder not sent yet
        # 4. Receiver wants notifications
        
        fifteen_min_ago = timezone.now() - timedelta(minutes=15)
        
        unread_messages = Message.objects.filter(
            is_read=False,
            email_reminder_sent=False,
            created_at__lte=fifteen_min_ago,
            receiver__notify_unread_messages=True,  # Check user preference
            receiver__is_active=True
        ).select_related('sender', 'receiver', 'conversation', 'conversation__listing')
        
        sent_count = 0
        error_count = 0
        
        for message in unread_messages:
            try:
                # Send email to receiver's personal email
                self.send_reminder_email(message)
                
                # Mark as sent
                message.email_reminder_sent = True
                message.save(update_fields=['email_reminder_sent'])
                
                sent_count += 1
                logger.info(f"Sent reminder to {message.receiver.personal_email} for message from {message.sender.email}")
                
            except Exception as e:
                error_count += 1
                logger.error(f"Failed to send reminder to {message.receiver.personal_email}: {str(e)}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Sent {sent_count} email reminders, {error_count} errors'
            )
        )
    
    def send_reminder_email(self, message):
        """Send email reminder for unread message"""
        receiver = message.receiver
        sender = message.sender
        listing = message.conversation.listing
        
        subject = f"Unread message from {sender.get_display_name()} on CredMarket"
        
        text_message = f"""
Hi {receiver.first_name},

You have an unread message from {sender.get_display_name()} about "{listing.title}":

"{message.content[:200]}{'...' if len(message.content) > 200 else ''}"

Reply now: {settings.SITE_URL}/messaging/conversation/{message.conversation.id}/

---
To stop receiving these reminders, update your preferences in your profile settings.
"""
        
        html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; }}
        .message-box {{ background: #f9fafb; padding: 20px; border-left: 4px solid #10b981; margin: 20px 0; border-radius: 4px; }}
        .listing-info {{ background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 15px 0; }}
        .button {{ display: inline-block; background: #10b981; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
        .footer {{ background: #f9fafb; padding: 20px; text-align: center; font-size: 12px; color: #6b7280; border-radius: 0 0 10px 10px; }}
        .timestamp {{ color: #6b7280; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💬 You Have an Unread Message</h1>
        </div>
        
        <div class="content">
            <p>Hi {receiver.first_name},</p>
            
            <p><strong>{sender.get_display_name()}</strong> sent you a message about <strong>{listing.title}</strong>:</p>
            
            <div class="message-box">
                <p style="margin: 0; color: #374151;">"{message.content[:300]}{'...' if len(message.content) > 300 else ''}"</p>
                <p class="timestamp" style="margin-top: 10px;">Sent {message.created_at.strftime('%b %d at %I:%M %p')}</p>
            </div>
            
            <div class="listing-info">
                <strong>{listing.title}</strong><br>
                <span style="color: #6b7280;">₹{listing.price:,.2f} • {listing.location}</span>
            </div>
            
            <p style="text-align: center;">
                <a href="{settings.SITE_URL}/messaging/conversation/{message.conversation.id}/" class="button">Reply Now</a>
            </p>
        </div>
        
        <div class="footer">
            <p>To stop receiving these reminders, update your preferences in your <a href="{settings.SITE_URL}/accounts/edit-profile/">profile settings</a>.</p>
            <p>This is an automated message. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Send with timeout to prevent hanging
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[receiver.personal_email],  # Use personal email
            html_message=html_message,
            fail_silently=True,
            timeout=10,
        )
