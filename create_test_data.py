"""
Create dummy users and listings for testing
"""

import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credmarket.settings')
django.setup()

from django.contrib.auth import get_user_model
from companies.models import Company
from listings.models import Category, Listing
from django.utils.text import slugify

User = get_user_model()

def create_test_data():
    print("🚀 Creating test data...")
    
    # Get existing companies
    companies = list(Company.objects.filter(status='approved'))
    if not companies:
        print("❌ No approved companies found. Run setup_data.py first!")
        return
    
    # Get categories
    categories = list(Category.objects.all())
    if not categories:
        print("❌ No categories found. Run setup_data.py first!")
        return
    
    # Dummy user data
    first_names = ['Rahul', 'Priya', 'Arjun', 'Sneha', 'Vikram', 'Ananya', 'Rohan', 'Divya', 
                   'Karan', 'Ishita', 'Aditya', 'Neha', 'Siddharth', 'Pooja', 'Harsh']
    last_names = ['Sharma', 'Patel', 'Kumar', 'Singh', 'Reddy', 'Desai', 'Mehta', 'Gupta',
                  'Joshi', 'Nair', 'Malhotra', 'Rao', 'Shah', 'Verma', 'Kapoor']
    
    # Create 15 dummy users
    users_created = []
    print("\n👥 Creating dummy users...")
    
    for i in range(15):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        company = random.choice(companies)
        email = f"{first_name.lower()}.{last_name.lower()}{i}@{company.domain}"
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            print(f"⏭️  User {email} already exists, skipping...")
            continue
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password='testpass123',
            first_name=first_name,
            last_name=last_name,
            company=company,
            status='approved',
            email_verified=True,
            phone=f'+91{random.randint(7000000000, 9999999999)}'
        )
        users_created.append(user)
        print(f"✅ Created user: {first_name} {last_name} ({email})")
    
    if not users_created:
        # Use existing users if no new ones created
        users_created = list(User.objects.filter(status='approved', email_verified=True))[:15]
        print(f"📋 Using {len(users_created)} existing users")
    
    # Product templates for realistic listings
    products = {
        'Electronics': [
            {'title': 'iPhone 13 Pro 256GB', 'price': 65000, 'desc': 'Mint condition, all accessories included. Battery health 95%. No scratches.'},
            {'title': 'MacBook Air M1 2020', 'price': 75000, 'desc': 'Lightly used, 8GB RAM, 256GB SSD. Perfect for developers. Original box and charger.'},
            {'title': 'Sony WH-1000XM4 Headphones', 'price': 18000, 'desc': 'Best noise cancellation. Barely used, like new condition.'},
            {'title': 'iPad Pro 11" 2021', 'price': 55000, 'desc': 'With Apple Pencil and Magic Keyboard. Great for productivity.'},
            {'title': 'Samsung Galaxy S22 Ultra', 'price': 70000, 'desc': 'Excellent condition, S Pen included. All original accessories.'},
            {'title': 'Dell XPS 15 Laptop', 'price': 85000, 'desc': '16GB RAM, 512GB SSD, GTX 1650. Perfect for coding and gaming.'},
            {'title': 'AirPods Pro 2nd Gen', 'price': 19000, 'desc': 'Sealed box, brand new. Got as gift, already have one.'},
            {'title': 'LG 27" 4K Monitor', 'price': 28000, 'desc': 'IPS display, USB-C, perfect for WFH setup. Barely 3 months old.'},
        ],
        'Furniture': [
            {'title': 'Herman Miller Aeron Chair', 'price': 45000, 'desc': 'Office ergonomic chair, excellent back support. Barely used.'},
            {'title': 'Standing Desk Adjustable', 'price': 22000, 'desc': 'Electric height adjustment, spacious. Perfect for WFH.'},
            {'title': 'IKEA Sofa Bed', 'price': 18000, 'desc': 'Comfortable 3-seater, converts to bed. Moving sale.'},
            {'title': 'Bookshelf Oak Wood', 'price': 8000, 'desc': 'Solid wood, 6 shelves, excellent condition.'},
            {'title': 'Dining Table Set', 'price': 25000, 'desc': 'Table + 6 chairs, modern design, glass top.'},
        ],
        'Books': [
            {'title': 'Clean Code by Robert Martin', 'price': 400, 'desc': 'Must-read for developers. Great condition.'},
            {'title': 'Designing Data-Intensive Apps', 'price': 600, 'desc': 'System design bible. Highlights and notes included.'},
            {'title': 'Atomic Habits by James Clear', 'price': 300, 'desc': 'Life-changing book. Read once, excellent condition.'},
            {'title': 'The Pragmatic Programmer', 'price': 500, 'desc': 'Classic programming book, like new.'},
            {'title': 'Sapiens by Yuval Harari', 'price': 350, 'desc': 'Fascinating read about human history.'},
        ],
        'Sports': [
            {'title': 'Yonex Badminton Racket', 'price': 3500, 'desc': 'Professional grade, barely used. Comes with cover.'},
            {'title': 'Cricket Bat SS TON', 'price': 8000, 'desc': 'English willow, well-knocked. Great for leather ball.'},
            {'title': 'Gym Dumbbells Set 20kg', 'price': 4000, 'desc': 'Adjustable weights, perfect for home gym.'},
            {'title': 'Trek Mountain Bike', 'price': 35000, 'desc': '21-speed, disc brakes, excellent condition. Serviced recently.'},
            {'title': 'Yoga Mat Premium', 'price': 1200, 'desc': 'Extra thick, non-slip, eco-friendly material.'},
        ],
        'Fashion': [
            {'title': 'Ray-Ban Aviator Sunglasses', 'price': 4500, 'desc': 'Original, with case and certificate. Barely worn.'},
            {'title': 'Levi\'s Denim Jacket', 'price': 2800, 'desc': 'Size L, classic blue, excellent condition.'},
            {'title': 'Nike Air Max Shoes', 'price': 6000, 'desc': 'Size 9, worn twice, perfect condition.'},
            {'title': 'Fossil Smartwatch', 'price': 12000, 'desc': 'Gen 6, all features working, with box.'},
            {'title': 'Zara Winter Coat', 'price': 3500, 'desc': 'Size M, warm and stylish, like new.'},
        ],
        'Home & Kitchen': [
            {'title': 'Philips Air Fryer', 'price': 7500, 'desc': 'Digital, 4.1L capacity, barely used. Healthy cooking!'},
            {'title': 'Dyson Vacuum Cleaner', 'price': 18000, 'desc': 'Cordless, powerful suction, 2 years old.'},
            {'title': 'Instant Pot Duo', 'price': 6000, 'desc': '7-in-1 pressure cooker, perfect condition.'},
            {'title': 'Coffee Machine Nespresso', 'price': 9000, 'desc': 'Makes perfect coffee, includes frother.'},
            {'title': 'Air Purifier Xiaomi', 'price': 8500, 'desc': 'HEPA filter, perfect for Delhi pollution.'},
        ],
    }
    
    cities = ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune', 'Chennai', 'Gurgaon', 'Noida']
    conditions = ['new', 'like_new', 'good', 'fair']
    
    # Create listings
    print("\n📦 Creating dummy listings...")
    listings_created = 0
    
    for category in categories:
        if category.name in products:
            product_list = products[category.name]
            
            for product in product_list:
                seller = random.choice(users_created)
                
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
                if random.random() > 0.8:
                    listing.is_featured = True
                    listing.save()
                
                listings_created += 1
                print(f"✅ Created listing: {product['title']} by {seller.first_name}")
    
    print(f"\n🎉 Test data creation complete!")
    print(f"📊 Summary:")
    print(f"   - Users created: {len(users_created)}")
    print(f"   - Listings created: {listings_created}")
    print(f"\n💡 You can now login with any user:")
    print(f"   Email: [firstname].[lastname][number]@[company-domain]")
    print(f"   Password: testpass123")
    print(f"\n   Example: rahul.sharma0@google.com / testpass123")

if __name__ == '__main__':
    create_test_data()
