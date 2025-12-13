from django.core.management.base import BaseCommand
from companies.models import Company
from accounts.models import User
from companies.signals import send_approval_email


class Command(BaseCommand):
    help = 'Approve a waitlisted company and notify all users'

    def add_arguments(self, parser):
        parser.add_argument(
            'domain',
            type=str,
            help='Company domain to approve (e.g., tcs.com)'
        )

    def handle(self, *args, **options):
        domain = options['domain']
        
        try:
            company = Company.objects.get(domain=domain)
        except Company.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Company with domain "{domain}" not found'))
            return
        
        if company.status == 'approved':
            self.stdout.write(self.style.WARNING(f'Company "{company.name}" is already approved'))
        else:
            self.stdout.write(self.style.NOTICE(f'Approving company: {company.name} ({domain})'))
            self.stdout.write(self.style.NOTICE(f'Previous status: {company.status}'))
            
            # Get waitlisted users before changing status
            waitlisted_users = User.objects.filter(
                company=company,
                status='waitlist',
                email_verified=True
            )
            
            user_count = waitlisted_users.count()
            self.stdout.write(self.style.NOTICE(f'Found {user_count} waitlisted users'))
            
            if user_count == 0:
                self.stdout.write(self.style.WARNING('No waitlisted users to notify'))
            
            # Update company status
            company.status = 'approved'
            company.save()
            
            # Update users and send emails
            success_count = 0
            for user in waitlisted_users:
                user.status = 'approved'
                user.save()
                
                # Send email
                if send_approval_email(user, company):
                    success_count += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Sent email to {user.email}'))
                else:
                    self.stdout.write(self.style.ERROR(f'  ✗ Failed to send email to {user.email}'))
            
            self.stdout.write(self.style.SUCCESS(f'\n✓ Company approved!'))
            self.stdout.write(self.style.SUCCESS(f'✓ Updated {user_count} users to approved status'))
            self.stdout.write(self.style.SUCCESS(f'✓ Sent {success_count}/{user_count} approval emails'))
