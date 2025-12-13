"""
Health check views for monitoring
"""
from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import sys


def health_check(request):
    """
    Health check endpoint for monitoring services.
    Returns 200 OK if application is healthy.
    """
    health_status = {
        'status': 'healthy',
        'debug': settings.DEBUG,
        'python_version': sys.version,
        'database': 'disconnected'
    }
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        health_status['database'] = 'connected'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['database'] = f'error: {str(e)}'
        return JsonResponse(health_status, status=503)
    
    return JsonResponse(health_status)


def readiness_check(request):
    """
    Readiness check - returns 200 when app is ready to serve traffic
    """
    return JsonResponse({'status': 'ready'})


def liveness_check(request):
    """
    Liveness check - returns 200 if app is running
    """
    return JsonResponse({'status': 'alive'})
