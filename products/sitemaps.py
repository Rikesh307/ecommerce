from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Category
from django.utils import timezone

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at or obj.created_at

    def location(self, obj):
        return reverse('products:product_detail', args=[obj.slug])

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Category.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('products:category', args=[obj.slug])

class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    protocol = 'https'

    def items(self):
        return [
            'products:home',
            'products:product_list',
            'products:contact',
            'products:about',
            'products:faq',
            'products:shipping',
            'products:returns',
            'products:privacy',
            'products:terms',
        ]

    def location(self, item):
        return reverse(item)
