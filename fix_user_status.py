#!/usr/bin/env python
"""
Fix user status for users with approved companies
Run this to ensure users with approved companies and verified emails can create listings
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credmarket.settings')
django.setup()

from accounts.models import User
from companies.models import Company

def fix_user_statuses():
    """Fix user statuses for approved companies"""
    
    # Get all users with approved companies but wrong status
    users_to_fix = User.objects.filter(
        company__status='approved',
        email_verified=True
    ).exclude(status='approved')
    
    print(f"Found {users_to_fix.count()} users to fix:")
    
    for user in users_to_fix:
        old_status = user.status
        user.status = 'approved'
        user.save()
        print(f"  ✅ {user.email}: {old_status} → approved (Company: {user.company.name})")
    
    # Also check for any users with approved status but unapproved companies
    mismatched = User.objects.filter(
        status='approved'
    ).exclude(company__status='approved')
    
    if mismatched.exists():
        print(f"\n⚠️  Found {mismatched.count()} users with approved status but unapproved companies:")
        for user in mismatched:
            company_status = user.company.status if user.company else 'No company'
            company_name = user.company.name if user.company else 'N/A'
            print(f"  {user.email} - status: {user.status}, company: {company_name}, company status: {company_status}")
    
    print("\n✅ Done!")

if __name__ == '__main__':
    fix_user_statuses()
