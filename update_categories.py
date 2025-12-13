# Script to update categories with new order and add Rent category

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credmarket.settings')
django.setup()

from listings.models import Category

# Updated categories with new order - Top 3: Vehicles, Rent, Real Estate
categories = [
    {'name': 'Vehicles', 'icon': 'fas fa-car', 'order': 1},
    {'name': 'Rent', 'icon': 'fas fa-home', 'order': 2},
    {'name': 'Real Estate', 'icon': 'fas fa-building', 'order': 3},
    {'name': 'Electronics', 'icon': 'fas fa-laptop', 'order': 4},
    {'name': 'Furniture', 'icon': 'fas fa-couch', 'order': 5},
    {'name': 'Home Appliances', 'icon': 'fas fa-blender', 'order': 6},
    {'name': 'Books', 'icon': 'fas fa-book', 'order': 7},
    {'name': 'Clothing', 'icon': 'fas fa-tshirt', 'order': 8},
    {'name': 'Sports & Fitness', 'icon': 'fas fa-dumbbell', 'order': 9},
    {'name': 'Others', 'icon': 'fas fa-box', 'order': 10},
]

print("🔄 Updating categories...")

for cat_data in categories:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={
            'icon': cat_data['icon'],
            'order': cat_data['order'],
            'is_active': True
        }
    )
    
    if not created:
        # Update existing category
        category.icon = cat_data['icon']
        category.order = cat_data['order']
        category.save()
        print(f"✅ Updated: {cat_data['name']} (order: {cat_data['order']})")
    else:
        print(f"🆕 Created: {cat_data['name']} (order: {cat_data['order']})")

print("\n🎉 Categories updated successfully!")
print("\nTop 3 Focus Categories:")
print("1. 🚗 Vehicles")
print("2. 🏠 Rent")
print("3. 🏢 Real Estate")

# Display all categories in order
print("\n📋 All Categories (in display order):")
for cat in Category.objects.filter(is_active=True).order_by('order'):
    print(f"   {cat.order}. {cat.icon} {cat.name}")
