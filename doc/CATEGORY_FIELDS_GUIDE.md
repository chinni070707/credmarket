# Category-Specific Fields Implementation Guide

## Overview
CredMarket now supports **subcategories** and **category-specific fields** to handle different types of listings within major categories like Vehicles, Rent, and Real Estate.

## How It Works

### 1. **Subcategories**
Categories can have child categories (subcategories) using the `parent` field:

```python
# Example hierarchy:
Vehicles (parent)
├── Cars (subcategory)
├── Bikes (subcategory)
├── Scooters (subcategory)
└── Bicycles (subcategory)
```

### 2. **Category-Specific Attributes**
Each listing has a `attributes` JSON field to store category-specific data:

```python
# Example for a Car listing:
listing.attributes = {
    "brand": "Honda",
    "model": "City",
    "year": "2020",
    "km_driven": "15000",
    "fuel_type": "Petrol",
    "transmission": "Manual",
    "owners": "1st Owner"
}

# Example for a 2 BHK Rent listing:
listing.attributes = {
    "furnishing": "Semi-Furnished",
    "bathrooms": "2",
    "deposit": "100000",
    "carpet_area": "1000",
    "floor_number": "5th Floor",
    "parking": "Car",
    "available_from": "2025-01-01"
}
```

## Current Subcategories

### 🚗 VEHICLES
- **Cars** - Brand, Model, Year, KM Driven, Fuel Type, Transmission, Owners
- **Bikes** - Brand, Model, Year, KM Driven, Owners
- **Scooters** - Brand, Model, Year, KM Driven
- **Bicycles** - Brand, Type
- **Commercial Vehicles** - (configure as needed)
- **Auto Parts** - (configure as needed)

### 🏠 RENT
- **1 BHK** - Furnishing, Bathrooms, Deposit, Carpet Area, Floor, Parking, Available From
- **2 BHK** - Furnishing, Bathrooms, Deposit, Carpet Area, Floor, Parking, Available From
- **3 BHK+** - Bedrooms, Furnishing, Bathrooms, Deposit, Carpet Area, Floor, Parking
- **Single Room** - Furnishing, Room Type, Deposit, Bathroom Type, Food, Available From
- **PG/Hostel** - Gender, Occupancy, Deposit, Food, AC, WiFi, Notice Period
- **Commercial Space** - (configure as needed)
- **Co-working Space** - (configure as needed)

### 🏢 REAL ESTATE
- **Apartments** - BHK, Bathrooms, Furnishing, Carpet Area, Floor, Facing, Parking, Age
- **Independent Houses** - Bedrooms, Bathrooms, Built-up Area, Plot Area, Floors, Facing
- **Villas** - (similar to Independent Houses)
- **Plots/Land** - Plot Area, Dimensions, Facing, Type, Boundary Wall
- **Commercial Buildings** - (configure as needed)
- **Farm Houses** - (configure as needed)

## Implementation in Forms

When creating a listing, the form should:

1. **Select main category** (e.g., Vehicles)
2. **Select subcategory** (e.g., Cars)
3. **Show category-specific fields** based on subcategory from `category_fields.py`
4. **Save to attributes JSON field**

### Example Form Flow:

```python
# In create_listing view:
from listings.category_fields import get_category_fields

# Get the selected category
category = Category.objects.get(id=request.POST.get('category'))

# Get category-specific fields configuration
category_fields = get_category_fields(category.name)

# Process and save attributes
attributes = {}
for field_name, field_config in category_fields.items():
    value = request.POST.get(f'attr_{field_name}')
    if value:
        attributes[field_name] = value

# Save to listing
listing.attributes = attributes
listing.save()
```

## Searching and Filtering

### Search by subcategory:
```python
# All cars
cars = Listing.objects.filter(category__name='Cars', status='active')

# All rent listings
rent_listings = Listing.objects.filter(category__parent__name='Rent', status='active')
```

### Filter by attributes:
```python
# Cars with Petrol fuel type
petrol_cars = Listing.objects.filter(
    category__name='Cars',
    attributes__fuel_type='Petrol'
)

# 2 BHK with parking
bhk_with_parking = Listing.objects.filter(
    category__name='2 BHK',
    attributes__parking__in=['Car', 'Both']
)

# Plots above 1000 sq ft
large_plots = Listing.objects.filter(
    category__name='Plots/Land',
    attributes__plot_area__gte=1000
)
```

## Display in Templates

```django
<!-- Show category-specific attributes -->
{% if listing.attributes %}
    <div class="attributes">
        {% for key, value in listing.attributes.items %}
            <div class="attribute">
                <strong>{{ key|title }}:</strong> {{ value }}
            </div>
        {% endfor %}
    </div>
{% endif %}
```

## Adding New Subcategories

1. Create via admin panel or script:
```python
Category.objects.create(
    name='New Subcategory',
    parent=parent_category,
    icon='fas fa-icon-name',
    order=7
)
```

2. Add field configuration in `category_fields.py`:
```python
CATEGORY_FIELDS = {
    'New Subcategory': {
        'field_name': {
            'type': 'text',  # or 'number', 'select', 'date'
            'label': 'Field Label',
            'required': True,
            'placeholder': 'Enter value...',
            'options': ['Option 1', 'Option 2']  # for select type
        },
    }
}
```

## Benefits

✅ **Flexible** - Easy to add new categories and fields without migrations
✅ **Searchable** - Can filter by any attribute using JSON queries
✅ **User-Friendly** - Relevant fields shown based on category selected
✅ **Scalable** - Supports unlimited categories and attributes
✅ **Type-Safe** - Field types ensure proper validation

## Next Steps

1. Update `create_listing.html` to show subcategory dropdown
2. Add JavaScript to dynamically show fields based on subcategory
3. Update `listing_detail.html` to display attributes nicely
4. Add attribute filters to search/browse pages
5. Create validation for required fields per category
