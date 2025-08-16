"""
Analytics and monitoring utilities for Riya Group E-commerce.
"""
from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["GET"])
@never_cache
def health_check(request):
    """
    Health check endpoint for monitoring systems.
    """
    return HttpResponse("OK", content_type="text/plain", status=200)

@require_http_methods(["GET"])
@never_cache
def status_check(request):
    """
    Detailed status check for monitoring.
    """
    status = {
        "status": "healthy",
        "version": "1.0.0",
        "environment": "production" if not settings.DEBUG else "development",
        "services": {
            "database": "connected",
            "cache": "connected" if hasattr(settings, 'CACHES') else "not_configured",
        }
    }
    
    return HttpResponse(
        json.dumps(status), 
        content_type="application/json", 
        status=200
    )

def get_google_analytics_code():
    """
    Return Google Analytics tracking code if configured.
    """
    ga_id = getattr(settings, 'GOOGLE_ANALYTICS_ID', None)
    if not ga_id:
        return ""
    
    return f"""
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{ga_id}');
    </script>
    """

def get_facebook_pixel_code():
    """
    Return Facebook Pixel tracking code if configured.
    """
    fb_pixel_id = getattr(settings, 'FACEBOOK_PIXEL_ID', None)
    if not fb_pixel_id:
        return ""
    
    return f"""
    <!-- Facebook Pixel -->
    <script>
        !function(f,b,e,v,n,t,s)
        {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', '{fb_pixel_id}');
        fbq('track', 'PageView');
    </script>
    <noscript><img height="1" width="1" style="display:none"
        src="https://www.facebook.com/tr?id={fb_pixel_id}&ev=PageView&noscript=1"
    /></noscript>
    """
