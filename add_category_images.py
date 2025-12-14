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
    # Parent Categories
    'Electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=300&fit=crop',
    'Furniture': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=300&fit=crop',
    'Vehicles': 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=400&h=300&fit=crop',
    'Books': 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400&h=300&fit=crop',
    'Real Estate': 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400&h=300&fit=crop',
    'Rent': 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400&h=300&fit=crop',
    
    # Vehicle Subcategories
    'Cars': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400&h=300&fit=crop',
    'Bikes': 'https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=400&h=300&fit=crop',
    'Scooters': 'https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?w=400&h=300&fit=crop',
    'Bicycles': 'https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=400&h=300&fit=crop',
    'Commercial Vehicles': 'https://images.unsplash.com/photo-1615906655593-ad0386982a0f?w=400&h=300&fit=crop',
    'Auto Parts': 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=400&h=300&fit=crop',
    
    # Real Estate Subcategories
    'Apartments': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400&h=300&fit=crop',
    'Independent Houses': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400&h=300&fit=crop',
    'Villas': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=400&h=300&fit=crop',
    'Plots/Land': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=400&h=300&fit=crop',
    'Commercial Buildings': 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400&h=300&fit=crop',
    'Farm Houses': 'https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=400&h=300&fit=crop',
    
    # Rent Subcategories
    '1 BHK': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400&h=300&fit=crop',
    '2 BHK': 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400&h=300&fit=crop',
    '3 BHK+': 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=400&h=300&fit=crop',
    'Single Room': 'https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=400&h=300&fit=crop',
    'PG/Hostel': 'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=400&h=300&fit=crop',
    'Commercial Space': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=400&h=300&fit=crop',
    'Co-working Space': 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=400&h=300&fit=crop',
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
