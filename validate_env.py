#!/usr/bin/env python
"""
Startup validation script to check all settings before deployment
"""
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def validate_environment():
    """Validate all required environment variables"""
    errors = []
    warnings = []
    
    # Required in production
    if os.environ.get('DEBUG', 'True').lower() == 'false':
        logger.info("Running in PRODUCTION mode")
        
        # Check critical settings
        if not os.environ.get('SECRET_KEY'):
            errors.append("SECRET_KEY is not set")
        elif os.environ.get('SECRET_KEY') == 'django-insecure-change-this-in-production':
            errors.append("SECRET_KEY is using default insecure value")
            
        if not os.environ.get('DATABASE_URL'):
            errors.append("DATABASE_URL is not set")
            
        if not os.environ.get('ALLOWED_HOSTS'):
            errors.append("ALLOWED_HOSTS is not set")
        else:
            logger.info(f"ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS')}")
            
        if not os.environ.get('CSRF_TRUSTED_ORIGINS'):
            warnings.append("CSRF_TRUSTED_ORIGINS is not set")
        else:
            logger.info(f"CSRF_TRUSTED_ORIGINS: {os.environ.get('CSRF_TRUSTED_ORIGINS')}")
            
        if not os.environ.get('EMAIL_HOST_PASSWORD'):
            warnings.append("EMAIL_HOST_PASSWORD is not set - email functionality will not work")
            
        if not os.environ.get('ADMIN_PASSWORD'):
            warnings.append("ADMIN_PASSWORD is not set - using default password")
    else:
        logger.info("Running in DEVELOPMENT mode")
    
    # Display results
    if errors:
        logger.error("VALIDATION FAILED - Critical errors found:")
        for error in errors:
            logger.error(f"  ❌ {error}")
        sys.exit(1)
    
    if warnings:
        logger.warning("Warnings found:")
        for warning in warnings:
            logger.warning(f"  ⚠️  {warning}")
    
    logger.info("✅ Environment validation passed")
    
    # Log all environment variables (excluding sensitive ones)
    logger.info("Environment variables:")
    for key in sorted(os.environ.keys()):
        if any(secret in key.upper() for secret in ['SECRET', 'PASSWORD', 'KEY', 'TOKEN']):
            logger.info(f"  {key}: ***HIDDEN***")
        else:
            logger.info(f"  {key}: {os.environ.get(key)}")

if __name__ == '__main__':
    validate_environment()
