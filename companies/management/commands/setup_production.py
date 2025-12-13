from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from companies.models import Company
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Setup production environment with initial data'

    def handle(self, *args, **kwargs):
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Creating superuser...')
            User.objects.create_superuser(
                username='admin',
                email='admin@credmarket.com',
                password=os.environ.get('ADMIN_PASSWORD', 'changeme123')
            )
            self.stdout.write(self.style.SUCCESS('Superuser created'))
        else:
            self.stdout.write('Superuser already exists')

        # Add companies if none exist
        if Company.objects.count() == 0:
            self.stdout.write('Adding top companies...')
            exec(open('add_top_companies.py').read())
            self.stdout.write(self.style.SUCCESS(f'Added {Company.objects.count()} companies'))
        else:
            self.stdout.write(f'{Company.objects.count()} companies already exist')
