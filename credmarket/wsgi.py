"""
WSGI config for credmarket project.
"""

import os
import logging
import traceback

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credmarket.settings')

try:
    from django.core.wsgi import get_wsgi_application
    logger.info("Starting WSGI application...")
    application = get_wsgi_application()
    logger.info("WSGI application started successfully")
except Exception as e:
    logger.error(f"CRITICAL ERROR during WSGI startup: {str(e)}")
    logger.error(f"Traceback:\n{traceback.format_exc()}")
    raise
