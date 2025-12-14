"""
Management command to create dummy listings for development/testing.
Only works when DEBUG=True to prevent accidental use in production.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from listings.models import Listing, Category, ListingImage
from companies.models import Company
import random
import os
import requests
from io import BytesIO

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates dummy listings for development or pre-launch mode (DEBUG=True or PRELAUNCH_MODE=true)'

    # Image URLs from Unsplash (free stock photos)
    IMAGE_URLS = {
        'electronics': [
            'https://images.unsplash.com/photo-1592286927505-b7a51177c8e4?w=800',  # iPhone
            'https://images.unsplash.com/photo-1611472173362-3f53dbd65d80?w=800',  # iPhone 2
            'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800',  # MacBook
            'https://images.unsplash.com/photo-1484788984921-03950022c9ef?w=800',  # MacBook 2
            'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800',  # Headphones
            'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800',  # Headphones 2
        ],
        'real_estate': [
            'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800',  # Modern house
            'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800',  # House exterior
            'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800',  # Living room
            'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800',  # Kitchen
            'https://images.unsplash.com/photo-1600607687644-c7171b42498b?w=800',  # Bedroom
            'https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=800',  # Bathroom
        ],
        'rental': [
            'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800',  # Apartment living
            'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800',  # Bedroom
            'https://images.unsplash.com/photo-1556912172-45b7abe8b7e1?w=800',  # Kitchen
            'https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=800',  # Balcony view
            'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800',  # Bathroom
            'https://images.unsplash.com/photo-1556912173-46c336c7fd55?w=800',  # Dining area
        ]
    }

    def download_image(self, url):
        """Download image from URL and return ContentFile"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return ContentFile(response.content)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'    ⚠️  Failed to download image: {e}'))
            return None

    def add_images_to_listing(self, listing, image_urls, category_type):
        """Add 4 images to a listing"""
        images_added = 0
        for i, url in enumerate(image_urls[:4]):  # Only use first 4 URLs
            image_content = self.download_image(url)
            if image_content:
                filename = f'{listing.slug}-{i+1}.jpg'
                ListingImage.objects.create(
                    listing=listing,
                    image=image_content,
                    order=i,
                    caption=f'{listing.title} - Image {i+1}'
                )
                # Save the image with proper filename
                listing_image = ListingImage.objects.filter(listing=listing, order=i).first()
                if listing_image:
                    listing_image.image.save(filename, image_content, save=True)
                    images_added += 1
        
        return images_added

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
        total_images = 0

        # Create Electronics listings
        self.stdout.write(self.style.WARNING('\n📱 Creating Electronics listings...'))
        for idx, data in enumerate(electronics_data):
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
                # Add images
                self.stdout.write('    📸 Downloading images...')
                image_urls = self.IMAGE_URLS['electronics'][idx*2:(idx*2)+4]  # Get 4 unique images
                images_added = self.add_images_to_listing(listing, image_urls, 'electronics')
                total_images += images_added
                self.stdout.write(self.style.SUCCESS(f'    ✅ Added {images_added} images'))

        # Create Real Estate listings
        self.stdout.write(self.style.WARNING('\n🏠 Creating Real Estate listings...'))
        for idx, data in enumerate(real_estate_data):
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
                # Add images
                self.stdout.write('    📸 Downloading images...')
                image_urls = self.IMAGE_URLS['real_estate'][idx*2:(idx*2)+4]  # Get 4 unique images
                images_added = self.add_images_to_listing(listing, image_urls, 'real_estate')
                total_images += images_added
                self.stdout.write(self.style.SUCCESS(f'    ✅ Added {images_added} images'))

        # Create Rental listings
        self.stdout.write(self.style.WARNING('\n🏢 Creating Rental listings...'))
        for idx, data in enumerate(rental_data):
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
                # Add images
                self.stdout.write('    📸 Downloading images...')
                image_urls = self.IMAGE_URLS['rental'][idx*2:(idx*2)+4]  # Get 4 unique images
                images_added = self.add_images_to_listing(listing, image_urls, 'rental')
                total_images += images_added
                self.stdout.write(self.style.SUCCESS(f'    ✅ Added {images_added} images'))

        self.stdout.write(self.style.SUCCESS(
            f'\n🎉 Successfully created {created_count} dummy listings with {total_images} images!'
        ))
        self.stdout.write(self.style.WARNING(
            '⚠️  Remember: These are dummy listings for development only.'
        ))
        self.stdout.write(self.style.WARNING(
            '💡 To remove them, delete all listings from user: dummy@example.com'
        ))
