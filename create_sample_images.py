"""
Generate placeholder images for listings using PIL
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credmarket.settings')
django.setup()

from PIL import Image, ImageDraw, ImageFont
from listings.models import Listing, ListingImage
import random

# Create media/listings directory if it doesn't exist
os.makedirs('media/listings', exist_ok=True)

def create_placeholder_image(text, filename, color):
    """Create a simple placeholder image with text"""
    img = Image.new('RGB', (800, 600), color=color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, fallback to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((800 - text_width) // 2, (600 - text_height) // 2)
    
    # Draw text
    draw.text(position, text, fill='white', font=font)
    
    # Save image
    img.save(f'media/listings/{filename}')
    print(f"Created: {filename}")

# Color palette for different categories
colors = [
    '#3B82F6',  # Blue
    '#10B981',  # Green
    '#F59E0B',  # Orange
    '#EF4444',  # Red
    '#8B5CF6',  # Purple
    '#EC4899',  # Pink
    '#6366F1',  # Indigo
    '#14B8A6',  # Teal
]

print("Creating placeholder images...")

# Get all listings without images
listings = Listing.objects.all()
created_count = 0

for listing in listings:
    # Check if listing already has images
    if listing.images.exists():
        print(f"Skipping {listing.title} - already has images")
        continue
    
    # Create 2-4 random images per listing
    num_images = random.randint(2, 4)
    
    for i in range(num_images):
        filename = f"{listing.slug}-{i+1}.jpg"
        color = random.choice(colors)
        
        # Create image with listing title
        create_placeholder_image(
            f"{listing.title}\nImage {i+1}",
            filename,
            color
        )
        
        # Create database record
        ListingImage.objects.create(
            listing=listing,
            image=f'listings/{filename}',
            order=i,
            caption=f"Image {i+1}"
        )
        created_count += 1

print(f"\n✅ Created {created_count} placeholder images for {listings.count()} listings!")
print(f"Images saved to: media/listings/")
