"""
Security utilities for Riya Group e-commerce platform.
"""
import hmac
import hashlib
import secrets
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def generate_secret_key():
    """Generate a secure Django secret key."""
    return secrets.token_urlsafe(50)

def secure_compare(a, b):
    """Securely compare two strings to prevent timing attacks."""
    return hmac.compare_digest(str(a), str(b))

def rate_limit_check(request, key, limit=10, window=60):
    """
    Simple rate limiting implementation.
    In production, use django-ratelimit or similar.
    """
    from django.core.cache import cache
    
    cache_key = f"rate_limit:{key}:{request.META.get('REMOTE_ADDR')}"
    current = cache.get(cache_key, 0)
    
    if current >= limit:
        raise SuspiciousOperation("Rate limit exceeded")
    
    cache.set(cache_key, current + 1, window)
    return True

def secure_view(login_required_flag=True):
    """
    Decorator for securing views with multiple security measures.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Rate limiting
            try:
                rate_limit_check(request, view_func.__name__)
            except SuspiciousOperation:
                logger.warning(f"Rate limit exceeded for {request.META.get('REMOTE_ADDR')} on {view_func.__name__}")
                raise
            
            return view_func(request, *args, **kwargs)
        
        # Apply security decorators
        if login_required_flag:
            wrapped_view = login_required(wrapped_view)
        wrapped_view = csrf_protect(wrapped_view)
        wrapped_view = never_cache(wrapped_view)
        
        return wrapped_view
    return decorator

class SecurityMiddleware:
    """
    Custom security middleware for additional protection.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Security headers
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        
        return response

    def process_exception(self, request, exception):
        """Log security-related exceptions."""
        if isinstance(exception, SuspiciousOperation):
            logger.warning(f"Suspicious operation from {request.META.get('REMOTE_ADDR')}: {exception}")
        return None
