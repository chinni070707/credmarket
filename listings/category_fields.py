"""
Category-specific field configurations for listings
This defines what additional fields should be shown for each category
"""

CATEGORY_FIELDS = {
    # VEHICLES
    'Cars': {
        'brand': {'type': 'text', 'label': 'Brand', 'required': True, 'placeholder': 'e.g., Honda, Toyota, Maruti'},
        'model': {'type': 'text', 'label': 'Model', 'required': True, 'placeholder': 'e.g., City, Innova'},
        'year': {'type': 'number', 'label': 'Year', 'required': True, 'placeholder': 'e.g., 2020'},
        'km_driven': {'type': 'number', 'label': 'KM Driven', 'required': True, 'placeholder': 'e.g., 15000'},
        'fuel_type': {'type': 'select', 'label': 'Fuel Type', 'required': True, 'options': ['Petrol', 'Diesel', 'CNG', 'Electric', 'Hybrid']},
        'transmission': {'type': 'select', 'label': 'Transmission', 'required': True, 'options': ['Manual', 'Automatic']},
        'owners': {'type': 'select', 'label': 'No. of Owners', 'required': True, 'options': ['1st Owner', '2nd Owner', '3rd Owner', '4+ Owners']},
    },
    'Bikes': {
        'brand': {'type': 'text', 'label': 'Brand', 'required': True, 'placeholder': 'e.g., Royal Enfield, Bajaj'},
        'model': {'type': 'text', 'label': 'Model', 'required': True, 'placeholder': 'e.g., Classic 350'},
        'year': {'type': 'number', 'label': 'Year', 'required': True, 'placeholder': 'e.g., 2021'},
        'km_driven': {'type': 'number', 'label': 'KM Driven', 'required': True, 'placeholder': 'e.g., 5000'},
        'owners': {'type': 'select', 'label': 'No. of Owners', 'required': True, 'options': ['1st Owner', '2nd Owner', '3rd Owner', '4+ Owners']},
    },
    'Scooters': {
        'brand': {'type': 'text', 'label': 'Brand', 'required': True, 'placeholder': 'e.g., Honda, TVS'},
        'model': {'type': 'text', 'label': 'Model', 'required': True, 'placeholder': 'e.g., Activa'},
        'year': {'type': 'number', 'label': 'Year', 'required': True, 'placeholder': 'e.g., 2022'},
        'km_driven': {'type': 'number', 'label': 'KM Driven', 'required': True, 'placeholder': 'e.g., 3000'},
    },
    'Bicycles': {
        'brand': {'type': 'text', 'label': 'Brand', 'required': False, 'placeholder': 'e.g., Hero, Firefox'},
        'type': {'type': 'select', 'label': 'Type', 'required': False, 'options': ['Mountain Bike', 'Road Bike', 'Hybrid', 'Electric', 'Kids']},
    },
    
    # RENT
    '1 BHK': {
        'furnishing': {'type': 'select', 'label': 'Furnishing', 'required': True, 'options': ['Unfurnished', 'Semi-Furnished', 'Fully Furnished']},
        'bathrooms': {'type': 'number', 'label': 'Bathrooms', 'required': True, 'placeholder': '1'},
        'deposit': {'type': 'number', 'label': 'Security Deposit (₹)', 'required': True, 'placeholder': 'e.g., 50000'},
        'carpet_area': {'type': 'number', 'label': 'Carpet Area (sq ft)', 'required': False, 'placeholder': 'e.g., 600'},
        'floor_number': {'type': 'text', 'label': 'Floor', 'required': False, 'placeholder': 'e.g., 3rd Floor'},
        'parking': {'type': 'select', 'label': 'Parking', 'required': False, 'options': ['None', 'Bike', 'Car', 'Both']},
        'available_from': {'type': 'date', 'label': 'Available From', 'required': False},
    },
    '2 BHK': {
        'furnishing': {'type': 'select', 'label': 'Furnishing', 'required': True, 'options': ['Unfurnished', 'Semi-Furnished', 'Fully Furnished']},
        'bathrooms': {'type': 'number', 'label': 'Bathrooms', 'required': True, 'placeholder': '2'},
        'deposit': {'type': 'number', 'label': 'Security Deposit (₹)', 'required': True, 'placeholder': 'e.g., 100000'},
        'carpet_area': {'type': 'number', 'label': 'Carpet Area (sq ft)', 'required': False, 'placeholder': 'e.g., 1000'},
        'floor_number': {'type': 'text', 'label': 'Floor', 'required': False, 'placeholder': 'e.g., 5th Floor'},
        'parking': {'type': 'select', 'label': 'Parking', 'required': False, 'options': ['None', 'Bike', 'Car', 'Both']},
        'available_from': {'type': 'date', 'label': 'Available From', 'required': False},
    },
    '3 BHK+': {
        'furnishing': {'type': 'select', 'label': 'Furnishing', 'required': True, 'options': ['Unfurnished', 'Semi-Furnished', 'Fully Furnished']},
        'bedrooms': {'type': 'number', 'label': 'Bedrooms', 'required': True, 'placeholder': '3'},
        'bathrooms': {'type': 'number', 'label': 'Bathrooms', 'required': True, 'placeholder': '2'},
        'deposit': {'type': 'number', 'label': 'Security Deposit (₹)', 'required': True, 'placeholder': 'e.g., 150000'},
        'carpet_area': {'type': 'number', 'label': 'Carpet Area (sq ft)', 'required': False, 'placeholder': 'e.g., 1500'},
        'floor_number': {'type': 'text', 'label': 'Floor', 'required': False, 'placeholder': 'e.g., 7th Floor'},
        'parking': {'type': 'select', 'label': 'Parking', 'required': False, 'options': ['None', 'Bike', 'Car', 'Both']},
        'available_from': {'type': 'date', 'label': 'Available From', 'required': False},
    },
    'Single Room': {
        'furnishing': {'type': 'select', 'label': 'Furnishing', 'required': True, 'options': ['Unfurnished', 'Semi-Furnished', 'Fully Furnished']},
        'room_type': {'type': 'select', 'label': 'Room Type', 'required': True, 'options': ['Single Occupancy', 'Double Occupancy', 'Triple Occupancy']},
        'deposit': {'type': 'number', 'label': 'Security Deposit (₹)', 'required': True, 'placeholder': 'e.g., 20000'},
        'attached_bathroom': {'type': 'select', 'label': 'Bathroom', 'required': False, 'options': ['Attached', 'Common']},
        'food_included': {'type': 'select', 'label': 'Food', 'required': False, 'options': ['Not Included', 'Breakfast', '2 Meals', '3 Meals']},
        'available_from': {'type': 'date', 'label': 'Available From', 'required': False},
    },
    'PG/Hostel': {
        'gender': {'type': 'select', 'label': 'For', 'required': True, 'options': ['Boys', 'Girls', 'Co-ed']},
        'occupancy': {'type': 'select', 'label': 'Occupancy', 'required': True, 'options': ['Single', 'Double', 'Triple', 'Multiple']},
        'deposit': {'type': 'number', 'label': 'Security Deposit (₹)', 'required': True, 'placeholder': 'e.g., 10000'},
        'food_included': {'type': 'select', 'label': 'Food', 'required': True, 'options': ['Not Included', 'Breakfast Only', '2 Meals', '3 Meals']},
        'ac_available': {'type': 'select', 'label': 'AC', 'required': False, 'options': ['Yes', 'No']},
        'wifi_available': {'type': 'select', 'label': 'WiFi', 'required': False, 'options': ['Yes', 'No']},
        'notice_period': {'type': 'text', 'label': 'Notice Period', 'required': False, 'placeholder': 'e.g., 1 month'},
    },
    
    # REAL ESTATE
    'Apartments': {
        'bedrooms': {'type': 'number', 'label': 'Bedrooms (BHK)', 'required': True, 'placeholder': '2'},
        'bathrooms': {'type': 'number', 'label': 'Bathrooms', 'required': True, 'placeholder': '2'},
        'furnishing': {'type': 'select', 'label': 'Furnishing', 'required': True, 'options': ['Unfurnished', 'Semi-Furnished', 'Fully Furnished']},
        'carpet_area': {'type': 'number', 'label': 'Carpet Area (sq ft)', 'required': True, 'placeholder': 'e.g., 1200'},
        'total_floors': {'type': 'number', 'label': 'Total Floors', 'required': False, 'placeholder': 'e.g., 15'},
        'floor_number': {'type': 'number', 'label': 'Floor Number', 'required': False, 'placeholder': 'e.g., 5'},
        'facing': {'type': 'select', 'label': 'Facing', 'required': False, 'options': ['North', 'South', 'East', 'West', 'North-East', 'North-West', 'South-East', 'South-West']},
        'parking': {'type': 'select', 'label': 'Parking', 'required': False, 'options': ['None', '1 Covered', '2 Covered', 'Open']},
        'age_of_property': {'type': 'select', 'label': 'Age of Property', 'required': False, 'options': ['Under Construction', '0-1 Year', '1-5 Years', '5-10 Years', '10+ Years']},
    },
    'Independent Houses': {
        'bedrooms': {'type': 'number', 'label': 'Bedrooms', 'required': True, 'placeholder': '3'},
        'bathrooms': {'type': 'number', 'label': 'Bathrooms', 'required': True, 'placeholder': '2'},
        'furnishing': {'type': 'select', 'label': 'Furnishing', 'required': True, 'options': ['Unfurnished', 'Semi-Furnished', 'Fully Furnished']},
        'built_up_area': {'type': 'number', 'label': 'Built-up Area (sq ft)', 'required': True, 'placeholder': 'e.g., 2000'},
        'plot_area': {'type': 'number', 'label': 'Plot Area (sq ft)', 'required': False, 'placeholder': 'e.g., 2400'},
        'floors': {'type': 'number', 'label': 'Number of Floors', 'required': False, 'placeholder': 'e.g., 2'},
        'facing': {'type': 'select', 'label': 'Facing', 'required': False, 'options': ['North', 'South', 'East', 'West', 'North-East', 'North-West', 'South-East', 'South-West']},
        'parking': {'type': 'select', 'label': 'Parking', 'required': False, 'options': ['None', '1 Car', '2 Cars', '3+ Cars']},
    },
    'Plots/Land': {
        'plot_area': {'type': 'number', 'label': 'Plot Area (sq ft)', 'required': True, 'placeholder': 'e.g., 1200'},
        'plot_length': {'type': 'number', 'label': 'Length (ft)', 'required': False, 'placeholder': 'e.g., 30'},
        'plot_width': {'type': 'number', 'label': 'Width (ft)', 'required': False, 'placeholder': 'e.g., 40'},
        'facing': {'type': 'select', 'label': 'Facing', 'required': False, 'options': ['North', 'South', 'East', 'West', 'North-East', 'North-West', 'South-East', 'South-West']},
        'plot_type': {'type': 'select', 'label': 'Type', 'required': False, 'options': ['Residential', 'Commercial', 'Agricultural', 'Industrial']},
        'boundary_wall': {'type': 'select', 'label': 'Boundary Wall', 'required': False, 'options': ['Yes', 'No', 'Partial']},
    },
}


def get_category_fields(category_name):
    """
    Get the field configuration for a specific category
    Returns the fields dict or empty dict if not configured
    """
    return CATEGORY_FIELDS.get(category_name, {})


def get_field_label(category_name, field_name):
    """
    Get the display label for a field
    """
    fields = get_category_fields(category_name)
    if field_name in fields:
        return fields[field_name].get('label', field_name.replace('_', ' ').title())
    return field_name.replace('_', ' ').title()
