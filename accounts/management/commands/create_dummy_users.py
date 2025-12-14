"""
Management command to create dummy users for development/testing.
Only works when DEBUG=True or PRELAUNCH_MODE=true to prevent accidental use in production.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from companies.models import Company
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates dummy users for development or pre-launch mode (DEBUG=True or PRELAUNCH_MODE=true)'

    def handle(self, *args, **options):
        # Safety check - only allow in DEBUG mode or PRELAUNCH_MODE
        prelaunch_mode = os.getenv('PRELAUNCH_MODE', 'false').lower() == 'true'
        
        if not settings.DEBUG and not prelaunch_mode:
            self.stdout.write(self.style.ERROR(
                '❌ This command only works in DEBUG mode or when PRELAUNCH_MODE=true. '
                'Production environment detected. Aborting.'
            ))
            return

        mode = 'PRELAUNCH' if prelaunch_mode and not settings.DEBUG else 'DEBUG'
        self.stdout.write(self.style.WARNING(
            f'🏗️  Creating dummy users for testing ({mode} mode)...'
        ))

        # Get or create test companies
        tcs_company, _ = Company.objects.get_or_create(
            domain='tcs.com',
            defaults={
                'name': 'Tata Consultancy Services',
                'status': 'approved',
            }
        )
        
        infosys_company, _ = Company.objects.get_or_create(
            domain='infosys.com',
            defaults={
                'name': 'Infosys Limited',
                'status': 'approved',
            }
        )
        
        wipro_company, _ = Company.objects.get_or_create(
            domain='wipro.com',
            defaults={
                'name': 'Wipro Technologies',
                'status': 'approved',
            }
        )

        # Dummy users data
        dummy_users = [
            {
                'email': 'test.user@tcs.com',
                'first_name': 'Test',
                'last_name': 'User',
                'company': tcs_company,
                'password': 'TestPass123!',
            },
            {
                'email': 'john.doe@infosys.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'company': infosys_company,
                'password': 'TestPass123!',
            },
            {
                'email': 'jane.smith@wipro.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'company': wipro_company,
                'password': 'TestPass123!',
            },
            {
                'email': 'demo.buyer@tcs.com',
                'first_name': 'Demo',
                'last_name': 'Buyer',
                'company': tcs_company,
                'password': 'BuyerPass123!',
            },
            {
                'email': 'demo.seller@infosys.com',
                'first_name': 'Demo',
                'last_name': 'Seller',
                'company': infosys_company,
                'password': 'SellerPass123!',
            },
        ]

        created_count = 0
        existing_count = 0

        for user_data in dummy_users:
            email = user_data['email']
            password = user_data.pop('password')
            
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'company': user_data['company'],
                    'email_verified': True,
                    'status': 'active',
                }
            )
            
            if created:
                user.set_password(password)
                user.save()
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'  ✅ Created user: {email} (password: {password})'
                ))
            else:
                existing_count += 1
                self.stdout.write(self.style.WARNING(
                    f'  ⚠️  User already exists: {email}'
                ))

        # Summary
        self.stdout.write(self.style.SUCCESS(
            f'\n🎉 Summary:'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'  ✅ Created {created_count} new dummy users'
        ))
        if existing_count > 0:
            self.stdout.write(self.style.WARNING(
                f'  ⚠️  Skipped {existing_count} existing users'
            ))
        
        self.stdout.write(self.style.WARNING(
            '\n📝 Login Credentials:'
        ))
        self.stdout.write(self.style.WARNING(
            '  • test.user@tcs.com / TestPass123!'
        ))
        self.stdout.write(self.style.WARNING(
            '  • john.doe@infosys.com / TestPass123!'
        ))
        self.stdout.write(self.style.WARNING(
            '  • jane.smith@wipro.com / TestPass123!'
        ))
        self.stdout.write(self.style.WARNING(
            '  • demo.buyer@tcs.com / BuyerPass123!'
        ))
        self.stdout.write(self.style.WARNING(
            '  • demo.seller@infosys.com / SellerPass123!'
        ))
        
        self.stdout.write(self.style.WARNING(
            '\n⚠️  Remember: These are dummy users for testing only.'
        ))
        self.stdout.write(self.style.WARNING(
            '💡 To remove them, delete users with these email addresses from admin panel.'
        ))
