"""
Add more dummy listings - cars, lands, phones, gadgets
"""

import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credmarket.settings')
django.setup()

from django.contrib.auth import get_user_model
from listings.models import Category, Listing
from django.utils.text import slugify

User = get_user_model()

def add_more_listings():
    print("🚀 Adding more dummy listings...")
    
    # Get existing users
    users = list(User.objects.filter(status='approved', email_verified=True))
    if not users:
        print("❌ No users found. Run create_test_data.py first!")
        return
    
    # Get categories
    categories = {cat.name: cat for cat in Category.objects.all()}
    
    # More product listings
    new_products = {
        'Electronics': [
            {'title': 'iPhone 14 Pro Max 512GB', 'price': 110000, 'desc': 'Deep Purple, mint condition. Bought 6 months ago. AppleCare+ included. Zero scratches, always used with case and screen protector.'},
            {'title': 'iPhone 13 128GB Blue', 'price': 52000, 'desc': 'Excellent condition, battery health 98%. All original accessories with box. Selling due to upgrade.'},
            {'title': 'Samsung Galaxy Buds2 Pro', 'price': 12000, 'desc': 'Graphite color, barely used. Active noise cancellation, perfect for WFH calls. With charging case and extra tips.'},
            {'title': 'Samsung Galaxy Buds Live', 'price': 7500, 'desc': 'Mystic Bronze, unique bean shape. Great sound quality. Comes with original box and all accessories.'},
            {'title': 'OnePlus 11 5G 16GB', 'price': 55000, 'desc': 'Titan Black, flagship killer! Snapdragon 8 Gen 2, blazing fast. Barely 2 months old.'},
            {'title': 'Google Pixel 7 Pro', 'price': 58000, 'desc': 'Best camera phone! Obsidian color, 12GB RAM. Pure Android experience. Mint condition.'},
            {'title': 'Nothing Phone 2 12GB', 'price': 42000, 'desc': 'White color with glyph interface. Unique design, great performance. Like new condition.'},
            {'title': 'PlayStation 5 Digital', 'price': 45000, 'desc': 'Digital edition, 1TB. Barely used, with 2 controllers and 3 games. Perfect condition.'},
            {'title': 'Xbox Series X', 'price': 48000, 'desc': '1TB console with Game Pass Ultimate 6 months. Excellent for 4K gaming. All original accessories.'},
            {'title': 'Apple Watch Series 8 45mm', 'price': 38000, 'desc': 'Midnight aluminum, GPS + Cellular. Health tracking, always-on display. With multiple bands.'},
            {'title': 'GoPro Hero 11 Black', 'price': 35000, 'desc': '5.3K video, waterproof action camera. Perfect for adventure enthusiasts. With mounts and accessories.'},
            {'title': 'DJI Mini 3 Pro Drone', 'price': 52000, 'desc': '4K camera drone, foldable. Perfect for aerial photography. With extra batteries and carrying case.'},
            {'title': 'Kindle Paperwhite 11th Gen', 'price': 9000, 'desc': 'Waterproof e-reader, 8GB storage. Perfect for book lovers. Barely used, like new.'},
            {'title': 'iPad Air 5th Gen 256GB', 'price': 58000, 'desc': 'M1 chip, Space Gray. Perfect for productivity and creativity. With Apple Pencil 2nd gen.'},
            {'title': 'Samsung Tab S8 Ultra', 'price': 75000, 'desc': 'Flagship Android tablet, 14.6" AMOLED. Perfect for multitasking. With S Pen and keyboard cover.'},
        ],
        'Vehicles': [
            {'title': 'Maruti Swift VXI 2019', 'price': 550000, 'desc': 'Pearl white, single owner. 35,000 km driven. Well maintained, all services done at authorized center. Non-accidental. Insurance valid till Dec 2025.'},
            {'title': 'Hyundai i20 Sportz 2020', 'price': 720000, 'desc': 'Polar white, diesel variant. 28,000 km, first owner. Excellent fuel efficiency. Showroom condition. All documents clear.'},
            {'title': 'Honda City VX 2018', 'price': 850000, 'desc': 'Modern steel metallic, petrol automatic. 42,000 km. Family car, well maintained. New tyres replaced recently.'},
            {'title': 'Tata Nexon XZ Plus 2021', 'price': 950000, 'desc': 'Foliage green, turbo petrol. 18,000 km only! Under warranty. Top variant with sunroof. Like new condition.'},
            {'title': 'Mahindra XUV700 AX7 2022', 'price': 1850000, 'desc': 'Everest white, diesel AWD. 12,000 km. Premium SUV with all features. Under manufacturer warranty. Pristine condition.'},
            {'title': 'Royal Enfield Classic 350', 'price': 145000, 'desc': 'Stealth black, 2021 model. 8,500 km. Well maintained bike. New engine oil and service done. Perfect for long rides.'},
            {'title': 'TVS Apache RTR 160 4V', 'price': 95000, 'desc': 'Racing red, 2020 model. 15,000 km. Sporty bike, good condition. All papers clear.'},
            {'title': 'Honda Activa 6G', 'price': 65000, 'desc': 'Pearl white, 2022 model. 3,200 km only! Ladies driven, showroom condition. Perfect for city commute.'},
        ],
        'Real Estate': [
            {'title': '2 BHK Apartment HSR Layout', 'price': 8500000, 'desc': 'Spacious 1200 sqft flat in prime Bangalore location. East facing, well ventilated. Ready to move. Clear title.'},
            {'title': '3 BHK Flat Whitefield', 'price': 12500000, 'desc': 'Premium 1650 sqft apartment. Gated community with amenities - gym, pool, clubhouse. IT park proximity.'},
            {'title': 'Office Space Indiranagar', 'price': 15000000, 'desc': '1800 sqft commercial space. Ideal for startup/IT company. Prime location, 24/7 security. Furnished option available.'},
            {'title': 'Agricultural Land 2 Acres', 'price': 5500000, 'desc': 'Fertile land near Mysore highway. Good water source. Perfect for organic farming. Clear documentation.'},
            {'title': 'Plot 30x40 Electronic City', 'price': 4200000, 'desc': 'BMRDA approved plot. Electricity and water connection available. Peaceful residential area. Ready for construction.'},
            {'title': 'Villa 4 BHK Sarjapur Road', 'price': 22500000, 'desc': 'Luxury villa 2800 sqft with private garden. Gated community, modern amenities. Premium finishes throughout.'},
            {'title': 'Commercial Shop MG Road', 'price': 35000000, 'desc': '850 sqft shop in prime retail location. High footfall area. Perfect for cafe/retail business.'},
            {'title': 'Farmhouse 5 Acres Kanakapura', 'price': 18500000, 'desc': 'Beautiful farmhouse with mango orchard. 3 bedroom house, bore well. Perfect weekend getaway.'},
        ],
        'Home & Kitchen': [
            {'title': 'LG French Door Refrigerator', 'price': 58000, 'desc': '687L capacity, InstaView feature. Smart inverter compressor. 1 year old, excellent condition.'},
            {'title': 'Samsung Washing Machine', 'price': 28000, 'desc': '7kg front load, eco bubble technology. Energy efficient. Barely used, relocating sale.'},
            {'title': 'IFB Microwave Convection 30L', 'price': 12000, 'desc': 'Multi-stage cooking, auto-cook menus. Excellent for baking. Well maintained.'},
            {'title': 'Prestige Induction Cooktop', 'price': 3500, 'desc': 'Latest model with auto shut-off. Energy efficient cooking. Like new condition.'},
        ],
    }
    
    cities = ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune', 'Chennai', 'Gurgaon', 'Noida', 'Kolkata']
    conditions = ['new', 'like_new', 'good', 'fair']
    
    # Map category names
    category_mapping = {
        'Vehicles': 'Vehicles',
        'Real Estate': 'Real Estate',
        'Electronics': 'Electronics',
        'Home & Kitchen': 'Home & Kitchen',
    }
    
    listings_created = 0
    
    for product_category, product_list in new_products.items():
        # Find the matching category
        category_name = category_mapping.get(product_category)
        
        if category_name and category_name in categories:
            category = categories[category_name]
            
            for product in product_list:
                seller = random.choice(users)
                
                # Check if similar listing exists
                if Listing.objects.filter(title=product['title']).exists():
                    print(f"⏭️  Listing '{product['title']}' already exists, skipping...")
                    continue
                
                listing = Listing.objects.create(
                    seller=seller,
                    category=category,
                    title=product['title'],
                    slug=slugify(product['title'] + '-' + str(random.randint(1000, 9999))),
                    description=product['desc'],
                    price=Decimal(str(product['price'])),
                    condition=random.choice(conditions),
                    city=random.choice(cities),
                    state='India',
                    is_negotiable=random.choice([True, False]),
                    status='active'
                )
                
                # Randomly mark some as featured
                if random.random() > 0.85:
                    listing.is_featured = True
                    listing.save()
                
                listings_created += 1
                print(f"✅ Created: {product['title']} - ₹{product['price']:,}")
        else:
            print(f"⚠️  Category '{product_category}' not found in database")
    
    print(f"\n🎉 Additional listings created: {listings_created}")

if __name__ == '__main__':
    add_more_listings()
