"""
Management command to add images to categories.
Safe to run in production - skips categories that already have images.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from listings.models import Category
import os
import requests
from io import BytesIO


class Command(BaseCommand):
    help = 'Adds images to categories (safe for production - skips existing images)'

    # Category images from Unsplash
    CATEGORY_IMAGES = {
        'Electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400',  # Electronics
        'Real Estate': 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400',  # House
        'Vehicles': 'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=400',  # Car
        'Furniture': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400',  # Furniture
        'Home Appliances': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400',  # Appliances
        'Sports & Fitness': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400',  # Gym
        'Books & Media': 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400',  # Books
        'Fashion & Beauty': 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400',  # Fashion
        'Pets': 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=400',  # Pets
        'Services': 'https://images.unsplash.com/photo-1556761175-b413da4baf72?w=400',  # Services
        'Jobs': 'https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=400',  # Office
        'Rentals': 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400',  # Apartment
    }

    def download_image(self, url):
        """Download image from URL."""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return ContentFile(response.content)
            else:
                self.stdout.write(self.style.WARNING(f'Failed to download: {url} (Status: {response.status_code})'))
                return None
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Error downloading {url}: {str(e)}'))
            return None

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🖼️  Adding images to categories...'))

        updated_count = 0
        skipped_count = 0

        for category_name, image_url in self.CATEGORY_IMAGES.items():
            try:
                # Find category (case-insensitive)
                category = Category.objects.filter(name__iexact=category_name).first()
                
                if not category:
                    self.stdout.write(self.style.WARNING(f'⚠️  Category not found: {category_name}'))
                    skipped_count += 1
                    continue
                
                # Skip if already has image
                if category.image:
                    self.stdout.write(f'⏭️  Skipping {category_name} (already has image)')
                    skipped_count += 1
                    continue
                
                # Download and save image
                self.stdout.write(f'📥 Downloading image for {category_name}...')
                image_content = self.download_image(image_url)
                
                if image_content:
                    # Save image with proper filename
                    filename = f'{category.slug}.jpg'
                    category.image.save(filename, image_content, save=True)
                    self.stdout.write(self.style.SUCCESS(f'✅ Added image to {category_name}'))
                    updated_count += 1
                else:
                    self.stdout.write(self.style.WARNING(f'❌ Failed to add image to {category_name}'))
                    skipped_count += 1
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {category_name}: {str(e)}'))
                skipped_count += 1

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'🎉 Summary:'))
        self.stdout.write(f'  ✅ Updated: {updated_count} categories')
        self.stdout.write(f'  ⏭️  Skipped: {skipped_count} categories')
        self.stdout.write('='*50)
