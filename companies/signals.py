from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Company
from accounts.models import User


@receiver(pre_save, sender=Company)
def track_company_status_change(sender, instance, **kwargs):
    """Track the previous status before save"""
    if instance.pk:
        try:
            old_instance = Company.objects.get(pk=instance.pk)
            instance._previous_status = old_instance.status
        except Company.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=Company)
def notify_waitlisted_users_on_approval(sender, instance, created, **kwargs):
    """
    When a company status changes from 'waitlist' to 'approved',
    notify all waitlisted users and update their status.
    """
    # Only process if company status changed from waitlist to approved
    if not created and instance.status == 'approved':
        previous_status = getattr(instance, '_previous_status', None)
        
        # Only proceed if status changed from waitlist to approved
        if previous_status == 'waitlist':
            # Find all waitlisted users for this company
            waitlisted_users = User.objects.filter(
                company=instance,
                status='waitlist',
                email_verified=True
            )
            
            if waitlisted_users.exists():
                print(f"Found {waitlisted_users.count()} waitlisted users for {instance.domain}")
                
                # Update all users to approved status
                waitlisted_users.update(status='approved')
                
                # Send email to each user
                for user in waitlisted_users:
                    send_approval_email(user, instance)
                    print(f"Sent approval email to {user.email}")


def send_approval_email(user, company):
    """Send approval notification email to user"""
    subject = f'🎉 Your Company Has Been Approved on CredMarket!'
    
    message = f"""Hi {user.first_name},

Great news! {company.name} has been approved on CredMarket.

You can now login and start using the platform:
🔗 Login here: {settings.SITE_URL}/accounts/login/

What you can do now:
✅ Browse listings from verified colleagues
✅ Post items for sale
✅ Message other users safely
✅ Join India's most trusted corporate marketplace

Welcome to CredMarket!

Best regards,
The CredMarket Team

---
Questions? Reply to this email or contact support@credmarket.com
"""
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #fff; padding: 30px; border: 1px solid #e5e7eb; }}
            .button {{ display: inline-block; background: #10b981; color: white; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }}
            .checklist {{ background: #f0fdf4; padding: 20px; border-left: 4px solid #10b981; margin: 20px 0; }}
            .checklist li {{ margin: 10px 0; }}
            .footer {{ text-align: center; color: #6b7280; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0; font-size: 28px;">🎉 Company Approved!</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Welcome to CredMarket</p>
            </div>
            
            <div class="content">
                <p>Hi <strong>{user.first_name}</strong>,</p>
                
                <p>Great news! <strong>{company.name}</strong> has been approved on CredMarket.</p>
                
                <div style="text-align: center;">
                    <a href="{settings.SITE_URL}/accounts/login/" class="button">
                        🔐 Login Now
                    </a>
                </div>
                
                <div class="checklist">
                    <h3 style="margin-top: 0; color: #059669;">What you can do now:</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li>✅ Browse listings from verified colleagues</li>
                        <li>✅ Post items for sale</li>
                        <li>✅ Message other users safely</li>
                        <li>✅ Join India's most trusted corporate marketplace</li>
                    </ul>
                </div>
                
                <p>Your email (<strong>{user.email}</strong>) is already verified, so you can login immediately!</p>
                
                <p style="margin-top: 30px;">
                    <strong>Welcome to CredMarket!</strong><br>
                    The CredMarket Team
                </p>
            </div>
            
            <div class="footer">
                <p>Questions? Contact us at <a href="mailto:support@credmarket.com">support@credmarket.com</a></p>
                <p>This is an automated message. Please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email to {user.email}: {str(e)}")
        return False
