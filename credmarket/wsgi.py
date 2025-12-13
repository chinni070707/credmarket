"""
WSGI config for credmarket project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credmarket.settings')

application = get_wsgi_application()
