# Setup script for CredMarket
# This creates initial data: superuser, categories, and companies

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credmarket.settings')
django.setup()

from django.contrib.auth import get_user_model
from listings.models import Category
from companies.models import Company

User = get_user_model()

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@credmarket.in',
        password='admin123',
        first_name='Admin',
        last_name='User',
        status='approved',
        email_verified=True
    )
    print("✅ Superuser created: admin / admin123")
else:
    print("⚠️  Superuser already exists")

# Create Categories
categories = [
    {'name': 'Electronics', 'icon': 'fas fa-laptop', 'order': 1},
    {'name': 'Vehicles', 'icon': 'fas fa-car', 'order': 2},
    {'name': 'Real Estate', 'icon': 'fas fa-building', 'order': 3},
    {'name': 'Furniture', 'icon': 'fas fa-couch', 'order': 4},
    {'name': 'Books', 'icon': 'fas fa-book', 'order': 5},
    {'name': 'Clothing', 'icon': 'fas fa-tshirt', 'order': 6},
    {'name': 'Home Appliances', 'icon': 'fas fa-blender', 'order': 7},
    {'name': 'Sports & Fitness', 'icon': 'fas fa-dumbbell', 'order': 8},
    {'name': 'Others', 'icon': 'fas fa-box', 'order': 9},
]

for cat in categories:
    Category.objects.get_or_create(
        name=cat['name'],
        defaults={'icon': cat['icon'], 'order': cat['order']}
    )

print(f"✅ {len(categories)} categories created")

# Create FAANG + Top Indian Companies
companies = [
    {'name': 'Google', 'domain': 'google.com'},
    {'name': 'Amazon', 'domain': 'amazon.com'},
    {'name': 'Meta (Facebook)', 'domain': 'fb.com'},
    {'name': 'Apple', 'domain': 'apple.com'},
    {'name': 'Netflix', 'domain': 'netflix.com'},
    {'name': 'Microsoft', 'domain': 'microsoft.com'},
    {'name': 'Flipkart', 'domain': 'flipkart.com'},
    {'name': 'Paytm', 'domain': 'paytm.com'},
    {'name': 'Zomato', 'domain': 'zomato.com'},
    {'name': 'Swiggy', 'domain': 'swiggy.in'},
    {'name': 'Ola', 'domain': 'olacabs.com'},
    {'name': 'PhonePe', 'domain': 'phonepe.com'},
    {'name': 'Razorpay', 'domain': 'razorpay.com'},
    {'name': 'Freshworks', 'domain': 'freshworks.com'},
    {'name': 'Zoho', 'domain': 'zoho.com'},
]

for company in companies:
    Company.objects.get_or_create(
        domain=company['domain'],
        defaults={'name': company['name'], 'status': 'approved'}
    )

print(f"✅ {len(companies)} companies added to whitelist")

print("\n🎉 Setup complete!")
print("\n📝 Admin Credentials:")
print("   Email: admin@credmarket.in")
print("   Password: admin123")
print("\n🌐 Start server with: python manage.py runserver")
print("   Visit: http://localhost:8000")
print("   Admin: http://localhost:8000/admin")
