# Script to add subcategories for Vehicles, Rent, and Real Estate

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credmarket.settings')
django.setup()

from listings.models import Category

print("🔄 Adding subcategories for top focus categories...\n")

# Get parent categories
vehicles = Category.objects.get(name='Vehicles')
rent = Category.objects.get(name='Rent')
real_estate = Category.objects.get(name='Real Estate')

# VEHICLES Subcategories
vehicles_subs = [
    {'name': 'Cars', 'icon': 'fas fa-car', 'order': 1},
    {'name': 'Bikes', 'icon': 'fas fa-motorcycle', 'order': 2},
    {'name': 'Scooters', 'icon': 'fas fa-biking', 'order': 3},
    {'name': 'Bicycles', 'icon': 'fas fa-bicycle', 'order': 4},
    {'name': 'Commercial Vehicles', 'icon': 'fas fa-truck', 'order': 5},
    {'name': 'Auto Parts', 'icon': 'fas fa-cog', 'order': 6},
]

print("🚗 VEHICLES Subcategories:")
for sub in vehicles_subs:
    category, created = Category.objects.get_or_create(
        name=sub['name'],
        parent=vehicles,
        defaults={'icon': sub['icon'], 'order': sub['order'], 'is_active': True}
    )
    status = "🆕 Created" if created else "✅ Exists"
    print(f"   {status}: {sub['name']}")

# RENT Subcategories
rent_subs = [
    {'name': '1 BHK', 'icon': 'fas fa-door-open', 'order': 1},
    {'name': '2 BHK', 'icon': 'fas fa-door-open', 'order': 2},
    {'name': '3 BHK+', 'icon': 'fas fa-door-open', 'order': 3},
    {'name': 'Single Room', 'icon': 'fas fa-bed', 'order': 4},
    {'name': 'PG/Hostel', 'icon': 'fas fa-building', 'order': 5},
    {'name': 'Commercial Space', 'icon': 'fas fa-store', 'order': 6},
    {'name': 'Co-working Space', 'icon': 'fas fa-laptop-house', 'order': 7},
]

print("\n🏠 RENT Subcategories:")
for sub in rent_subs:
    category, created = Category.objects.get_or_create(
        name=sub['name'],
        parent=rent,
        defaults={'icon': sub['icon'], 'order': sub['order'], 'is_active': True}
    )
    status = "🆕 Created" if created else "✅ Exists"
    print(f"   {status}: {sub['name']}")

# REAL ESTATE Subcategories
real_estate_subs = [
    {'name': 'Apartments', 'icon': 'fas fa-building', 'order': 1},
    {'name': 'Independent Houses', 'icon': 'fas fa-home', 'order': 2},
    {'name': 'Villas', 'icon': 'fas fa-home', 'order': 3},
    {'name': 'Plots/Land', 'icon': 'fas fa-map', 'order': 4},
    {'name': 'Commercial Buildings', 'icon': 'fas fa-city', 'order': 5},
    {'name': 'Farm Houses', 'icon': 'fas fa-tractor', 'order': 6},
]

print("\n🏢 REAL ESTATE Subcategories:")
for sub in real_estate_subs:
    category, created = Category.objects.get_or_create(
        name=sub['name'],
        parent=real_estate,
        defaults={'icon': sub['icon'], 'order': sub['order'], 'is_active': True}
    )
    status = "🆕 Created" if created else "✅ Exists"
    print(f"   {status}: {sub['name']}")

print("\n🎉 All subcategories added successfully!")

# Show hierarchy
print("\n📋 Category Hierarchy:")
for parent in [vehicles, rent, real_estate]:
    print(f"\n{parent.icon} {parent.name}:")
    for sub in parent.subcategories.all().order_by('order'):
        print(f"   └─ {sub.icon} {sub.name}")
