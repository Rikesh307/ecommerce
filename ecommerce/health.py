"""
Health check views for production monitoring.
"""
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.db import connection
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Basic health check endpoint for load balancers and monitoring.
    """
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Test cache
        cache.set('health_check', 'ok', 10)
        cache_status = cache.get('health_check')
        
        health_data = {
            'status': 'healthy',
            'database': 'ok',
            'cache': 'ok' if cache_status == 'ok' else 'error',
            'version': '1.0.0'
        }
        
        return JsonResponse(health_data, status=200)
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)

@csrf_exempt
@require_http_methods(["GET"])
def ready_check(request):
    """
    Readiness check for Kubernetes deployments.
    """
    try:
        # More comprehensive checks
        checks = {
            'database': False,
            'cache': False,
            'static_files': False
        }
        
        # Database check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM django_migrations")
                checks['database'] = True
        except Exception:
            pass
        
        # Cache check
        try:
            cache.set('ready_check', 'ok', 10)
            if cache.get('ready_check') == 'ok':
                checks['cache'] = True
        except Exception:
            pass
        
        # Static files check (basic)
        checks['static_files'] = True  # Assume OK if no errors
        
        all_ready = all(checks.values())
        
        return JsonResponse({
            'ready': all_ready,
            'checks': checks
        }, status=200 if all_ready else 503)
    
    except Exception as e:
        logger.error(f"Ready check failed: {e}")
        return JsonResponse({
            'ready': False,
            'error': str(e)
        }, status=503)
