"""
Management command to create dummy listings for development/testing.
Only works when DEBUG=True to prevent accidental use in production.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from listings.models import Listing, Category
from companies.models import Company
import random
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates dummy listings for development or pre-launch mode (DEBUG=True or PRELAUNCH_MODE=true)'

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
            f'🏗️  Creating dummy listings for local development ({mode} mode)...'
        ))

        # Get or create a test user
        user, created = User.objects.get_or_create(
            email='dummy@example.com',
            defaults={
                'first_name': 'Demo',
                'last_name': 'User',
                'is_active': True,
                'email_verified': True,
            }
        )
        if created:
            user.set_password('dummypassword123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Created test user: {user.email}'))

        # Get or create categories
        electronics, _ = Category.objects.get_or_create(
            name='Electronics',
            defaults={'slug': 'electronics', 'is_active': True}
        )
        real_estate, _ = Category.objects.get_or_create(
            name='Real Estate',
            defaults={'slug': 'real-estate', 'is_active': True}
        )
        rentals, _ = Category.objects.get_or_create(
            name='Rent',
            defaults={'slug': 'rent', 'is_active': True}
        )

        cities = ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune', 'Chennai']
        conditions = ['new', 'like_new', 'good', 'fair']

        # Electronics listings
        electronics_data = [
            {
                'title': 'iPhone 14 Pro Max 256GB - Space Black - DUMMY',
                'description': 'Lightly used iPhone 14 Pro Max in excellent condition. Comes with original box, charger, and unused EarPods. Battery health 98%. No scratches on screen, minimal wear on edges. Always used with case and screen protector.',
                'price': 95000,
                'condition': 'like_new',
                'negotiable': True,
            },
            {
                'title': 'MacBook Pro M2 16" 32GB RAM 1TB SSD - DUMMY',
                'description': 'Barely used MacBook Pro M2 chip, perfect for developers and creators. 16-inch Liquid Retina XDR display, 32GB unified memory, 1TB SSD. Still under AppleCare warranty. Includes original packaging and all accessories.',
                'price': 225000,
                'condition': 'like_new',
                'negotiable': False,
            },
            {
                'title': 'Sony WH-1000XM5 Noise Cancelling Headphones - DUMMY',
                'description': 'Premium wireless headphones with industry-leading noise cancellation. Only 3 months old, mint condition. Comes with carrying case, cables, and adapter. Perfect for work from home professionals.',
                'price': 24000,
                'condition': 'like_new',
                'negotiable': True,
            },
        ]

        # Real Estate listings
        real_estate_data = [
            {
                'title': '3BHK Luxury Apartment in Whitefield - 1850 sqft - DUMMY',
                'description': '3 BHK luxury apartment in premium gated community. East facing, excellent ventilation, modular kitchen, wooden flooring. Amenities: swimming pool, gym, clubhouse, 24/7 security. Ready to move. Clear title.',
                'price': 12500000,
                'condition': 'new',
                'negotiable': True,
            },
            {
                'title': '2BHK Corner Flat in Koramangala - 1200 sqft - DUMMY',
                'description': 'Spacious 2BHK corner apartment with excellent natural light. Well-maintained building, covered parking, power backup. Near schools, hospitals, and metro station. Vastu compliant. Immediate possession available.',
                'price': 8500000,
                'condition': 'good',
                'negotiable': True,
            },
            {
                'title': 'Independent Villa in Sarjapur Road - 2400 sqft - DUMMY',
                'description': '4BHK independent villa with private garden and terrace. Modern architecture, premium fittings, solar panels installed. Gated community with club facilities. 10 mins from ORR. Perfect for families.',
                'price': 18000000,
                'condition': 'new',
                'negotiable': False,
            },
        ]

        # Rental listings
        rental_data = [
            {
                'title': '2BHK Fully Furnished Flat for Rent - HSR Layout - DUMMY',
                'description': 'Fully furnished 2BHK apartment available for rent. Includes bed, sofa, dining table, refrigerator, washing machine, AC in all rooms. Covered parking, 24/7 water, power backup. Vegetarian/Non-vegetarian both ok.',
                'price': 35000,
                'condition': 'good',
                'negotiable': True,
            },
            {
                'title': '1BHK Bachelor-friendly Flat - Marathahalli - DUMMY',
                'description': 'Spacious 1BHK apartment perfect for working professionals. Semi-furnished with kitchen appliances. Gym and parking available. Walking distance to tech parks. No brokerage, owner direct. Available from Jan 1st.',
                'price': 18000,
                'condition': 'good',
                'negotiable': True,
            },
            {
                'title': '3BHK Penthouse for Rent - Indiranagar - DUMMY',
                'description': 'Luxurious 3BHK penthouse with terrace garden and city view. Fully furnished with premium interiors. Swimming pool, gym, concierge services. Ideal for expats and senior management. Pet-friendly building.',
                'price': 75000,
                'condition': 'like_new',
                'negotiable': False,
            },
        ]

        created_count = 0

        # Create Electronics listings
        for data in electronics_data:
            city = random.choice(cities)
            listing, created = Listing.objects.get_or_create(
                title=data['title'],
                seller=user,
                defaults={
                    'description': data['description'],
                    'price': data['price'],
                    'category': electronics,
                    'condition': data['condition'],
                    'is_negotiable': data['negotiable'],
                    'city': city,
                    'location': f'{city}, Karnataka',
                    'status': 'active',
                    'state': 'Karnataka',
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✅ Created: {listing.title}'))

        # Create Real Estate listings
        for data in real_estate_data:
            city = random.choice(cities)
            listing, created = Listing.objects.get_or_create(
                title=data['title'],
                seller=user,
                defaults={
                    'description': data['description'],
                    'price': data['price'],
                    'category': real_estate,
                    'condition': data['condition'],
                    'is_negotiable': data['negotiable'],
                    'city': city,
                    'location': f'{city}, Karnataka',
                    'status': 'active',
                    'state': 'Karnataka',
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✅ Created: {listing.title}'))

        # Create Rental listings
        for data in rental_data:
            city = random.choice(cities)
            listing, created = Listing.objects.get_or_create(
                title=data['title'],
                seller=user,
                defaults={
                    'description': data['description'],
                    'price': data['price'],
                    'category': rentals,
                    'condition': data['condition'],
                    'is_negotiable': data['negotiable'],
                    'city': city,
                    'location': f'{city}, Karnataka',
                    'status': 'active',
                    'state': 'Karnataka',
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✅ Created: {listing.title}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n🎉 Successfully created {created_count} dummy listings!'
        ))
        self.stdout.write(self.style.WARNING(
            '⚠️  Remember: These are dummy listings for development only.'
        ))
        self.stdout.write(self.style.WARNING(
            '💡 To remove them, delete all listings from user: dummy@example.com'
        ))
