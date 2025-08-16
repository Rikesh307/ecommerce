"""
URL configuration for ecommerce project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap
from products.sitemaps import ProductSitemap, CategorySitemap, StaticSitemap
from products import views
from products.analytics import health_check, status_check

# Sitemap configuration
sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'static': StaticSitemap,
}

def robots_txt(request):
    """Serve robots.txt file"""
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Disallow admin and private areas",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Disallow: /cart/",
        "Disallow: /orders/",
        "",
        "# Allow important pages", 
        "Allow: /",
        "Allow: /products/",
        "Allow: /contact/",
        "",
        f"# Sitemap location",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
        "",
        "# Crawl-delay to be respectful",
        "Crawl-delay: 1"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    
    # Health checks for production monitoring
    path('health/', health_check, name='health_check'),
    path('status/', status_check, name='status_check'),

    # SEO URLs
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)