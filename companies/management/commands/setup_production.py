from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from companies.models import Company
import os
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Setup production environment with initial data'

    def handle(self, *args, **kwargs):
        logger.info("Starting production setup...")
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Creating superuser...')
            logger.info("Creating superuser account...")
            User.objects.create_superuser(
                username='admin',
                email='admin@credmarket.com',
                password=os.environ.get('ADMIN_PASSWORD', 'changeme123')
            )
            self.stdout.write(self.style.SUCCESS('Superuser created'))
            logger.info("Superuser created successfully")
        else:
            self.stdout.write('Superuser already exists')
            logger.info("Superuser already exists, skipping creation")

        # Add companies if none exist
        company_count = Company.objects.count()
        if company_count == 0:
            self.stdout.write('Adding top companies...')
            logger.info("Loading initial company data...")
            try:
                exec(open('add_top_companies.py').read())
                new_count = Company.objects.count()
                self.stdout.write(self.style.SUCCESS(f'Added {new_count} companies'))
                logger.info(f"Successfully added {new_count} companies")
            except Exception as e:
                logger.error(f"Error loading companies: {str(e)}")
                self.stdout.write(self.style.ERROR(f'Error loading companies: {str(e)}'))
        else:
            self.stdout.write(f'{company_count} companies already exist')
            logger.info(f"{company_count} companies already exist in database")
        
        logger.info("Production setup completed")
