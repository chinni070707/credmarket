"""
Create test user for debugging
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credmarket.settings')
django.setup()

from accounts.models import User
from companies.models import Company

# Create or get Cadence company
company, created = Company.objects.get_or_create(
    name='Cadence Design Systems',
    defaults={
        'domain': 'cadence.com',
        'status': 'approved'
    }
)
print(f"Company: {company.name} ({'created' if created else 'already exists'})")

# Create or update test user
email = 'john@cadence.com'
try:
    user = User.objects.get(email=email)
    print(f"User {email} already exists")
    # Update password
    user.set_password('password123')
    user.email_verified = True
    user.status = 'approved'
    user.company = company
    user.save()
    print(f"Updated password and verified email for {email}")
except User.DoesNotExist:
    user = User.objects.create_user(
        email=email,
        username=email,  # Use email as username
        password='password123',
        first_name='John',
        last_name='Doe',
        company=company,
        email_verified=True,
        status='approved',
        location='Bangalore',
        area='Koramangala'
    )
    print(f"Created new user: {email}")

print("\n✅ Test user ready!")
print(f"Email: {user.email}")
print(f"Password: password123")
print(f"Name: {user.first_name} {user.last_name}")
print(f"Company: {user.company.name if user.company else 'None'}")
print(f"Status: {user.status}")
print(f"Email Verified: {user.email_verified}")
