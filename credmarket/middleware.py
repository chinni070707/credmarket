"""
Custom middleware for error logging and debugging
"""
import logging
import traceback

logger = logging.getLogger(__name__)


class ErrorLoggingMiddleware:
    """
    Middleware to log all exceptions with full tracebacks
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Log all 500 errors
        if response.status_code == 500:
            logger.error(
                f"500 Error on {request.method} {request.path}\n"
                f"User: {request.user if hasattr(request, 'user') else 'Unknown'}\n"
                f"IP: {self.get_client_ip(request)}\n"
                f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}"
            )
        
        return response

    def process_exception(self, request, exception):
        """
        Log all exceptions with full traceback
        """
        logger.error(
            f"EXCEPTION CAUGHT: {type(exception).__name__}: {str(exception)}\n"
            f"Path: {request.method} {request.path}\n"
            f"User: {request.user if hasattr(request, 'user') else 'Unknown'}\n"
            f"IP: {self.get_client_ip(request)}\n"
            f"Full traceback:\n{traceback.format_exc()}"
        )
        # Return None to let Django's default error handling proceed
        return None

    @staticmethod
    def get_client_ip(request):
        """Get client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware:
    """
    Middleware to add security headers including Content Security Policy
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add Content Security Policy to prevent XSS attacks
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://unpkg.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
            "img-src 'self' data: https://res.cloudinary.com; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        
        # Additional security headers
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        
        return response
