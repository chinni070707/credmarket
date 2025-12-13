import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credmarket.settings')
django.setup()

from companies.models import Company

total = Company.objects.count()
approved = Company.objects.filter(status='approved').count()
waitlist = Company.objects.filter(status='waitlist').count()

print(f"Database Status:")
print(f"  Total companies: {total}")
print(f"  Approved: {approved}")
print(f"  Waitlist: {waitlist}")
print(f"\nSample approved companies:")
for company in Company.objects.filter(status='approved').order_by('name')[:15]:
    print(f"  ✓ {company.name} - {company.domain}")
