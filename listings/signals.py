from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Listing
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Listing)
def notify_company_members_new_listing(sender, instance, created, **kwargs):
    """
    Send email notification to company members when a new listing is created
    Only for active listings, not drafts
    """
    if not created or instance.status != 'active':
        return
    
    # Get seller's company
    if not instance.seller.company:
        return
    
    company = instance.seller.company
    
    # Get all users from the same company who want notifications (excluding the seller)
    from accounts.models import User
    users_to_notify = User.objects.filter(
        company=company,
        status='approved',
        is_active=True,
        notify_new_company_listings=True  # Check preference
    ).exclude(id=instance.seller.id)
    
    if not users_to_notify.exists():
        logger.info(f"No users to notify for new listing: {instance.title}")
        return
    
    # Email content
    subject = f"New {instance.category.name} listed at {company.name}"
    
    message = f"""
A colleague from {company.name} just listed a new item!

Item: {instance.title}
Category: {instance.category.name}
Price: ₹{instance.price:,.2f}{'(Negotiable)' if instance.is_negotiable else ''}
Condition: {instance.get_condition_display()}
Location: {instance.location}

Seller: {instance.seller.get_display_name()}

View listing: {settings.SITE_URL}/listings/{instance.slug}/

---
To stop receiving these notifications, update your preferences in your profile settings.
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
            .listing-details {{ background: #f9fafb; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .detail-row {{ margin: 10px 0; }}
            .label {{ font-weight: bold; color: #6b7280; }}
            .value {{ color: #111827; }}
            .price {{ font-size: 24px; color: #10b981; font-weight: bold; }}
            .button {{ display: inline-block; background: #10b981; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
            .footer {{ background: #f9fafb; padding: 20px; text-align: center; font-size: 12px; color: #6b7280; border-radius: 0 0 10px 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 New Item Listed at {company.name}</h1>
            </div>
            
            <div class="content">
                <p>Hi there!</p>
                
                <p>Your colleague <strong>{instance.seller.get_display_name()}</strong> just listed a new item on CredMarket:</p>
                
                <div class="listing-details">
                    <h2 style="margin-top: 0; color: #111827;">{instance.title}</h2>
                    
                    <div class="detail-row">
                        <span class="label">Category:</span>
                        <span class="value">{instance.category.name}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="price">₹{instance.price:,.2f}</span>
                        {'<span style="color: #6b7280; font-size: 14px;"> (Negotiable)</span>' if instance.is_negotiable else ''}
                    </div>
                    
                    <div class="detail-row">
                        <span class="label">Condition:</span>
                        <span class="value">{instance.get_condition_display()}</span>
                    </div>
                    
                    <div class="detail-row">
                        <span class="label">Location:</span>
                        <span class="value">{instance.location}</span>
                    </div>
                </div>
                
                <p style="text-align: center;">
                    <a href="{settings.SITE_URL}/listings/{instance.slug}/" class="button">View Listing</a>
                </p>
            </div>
            
            <div class="footer">
                <p>To stop receiving these notifications, update your preferences in your <a href="{settings.SITE_URL}/accounts/edit-profile/">profile settings</a>.</p>
                <p>This is an automated message. Please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Send to each user's personal email (async to avoid blocking)
    import threading
    
    def _send_notifications():
        for user in users_to_notify:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.personal_email],  # Use personal email
                    html_message=html_message,
                    fail_silently=True,
                    timeout=10,
                )
                logger.info(f"Sent new listing notification to {user.personal_email} for listing: {instance.title}")
            except Exception as e:
                logger.error(f"Failed to send new listing notification to {user.personal_email}: {str(e)}")
    
    # Run in background thread
    threading.Thread(target=_send_notifications, daemon=True).start()
