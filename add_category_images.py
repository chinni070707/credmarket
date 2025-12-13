"""
Script to add category images using Unsplash URLs (free stock photos)
Run: python add_category_images.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credmarket.settings')
django.setup()

from listings.models import Category

# Beautiful stock images from Unsplash (royalty-free)
CATEGORY_IMAGES = {
    'Electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=300&fit=crop',
    'Furniture': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=300&fit=crop',
    'Vehicles': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=400&h=300&fit=crop',
    'Books': 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400&h=300&fit=crop',
    'Fashion': 'https://images.unsplash.com/photo-1445205170230-053b83016050?w=400&h=300&fit=crop',
    'Sports': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400&h=300&fit=crop',
    'Home & Garden': 'https://images.unsplash.com/photo-1556912167-f556f1f39fdf?w=400&h=300&fit=crop',
    'Mobile Phones': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop',
    'Laptops': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop',
    'Cameras': 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400&h=300&fit=crop',
    'Bikes': 'https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=400&h=300&fit=crop',
    'Cars': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400&h=300&fit=crop',
    'Real Estate': 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400&h=300&fit=crop',
    'Jobs': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400&h=300&fit=crop',
    'Services': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=300&fit=crop',
}

def download_and_save_image(url, category):
    """Download image from URL and save to category"""
    import requests
    from django.core.files.base import ContentFile
    from io import BytesIO
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Get filename from category name
        filename = f"{category.slug}.jpg"
        
        # Save to category
        category.image.save(
            filename,
            ContentFile(response.content),
            save=True
        )
        return True
    except Exception as e:
        print(f"  ❌ Error downloading image: {e}")
        return False

def main():
    print("🖼️  Adding images to categories...\n")
    
    updated = 0
    for category_name, image_url in CATEGORY_IMAGES.items():
        try:
            category = Category.objects.get(name=category_name)
            print(f"📸 Processing: {category_name}")
            
            if download_and_save_image(image_url, category):
                print(f"  ✅ Image added successfully")
                updated += 1
            
        except Category.DoesNotExist:
            print(f"  ⚠️  Category '{category_name}' not found, skipping")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n✨ Done! Updated {updated} categories with images")
    print("\n💡 Tip: You can also upload images manually via Django admin")

if __name__ == '__main__':
    main()
