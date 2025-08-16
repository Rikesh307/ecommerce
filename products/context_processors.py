from .models import Category
from django.db.models import Count, Q


def categories_context(request):
    """
    Add categories context to all templates with product counts
    SDLC Enhancement: Performance-optimized category loading
    """
    # Get categories with product counts (SDLC Performance Optimization)
    categories = Category.objects.filter(
        is_active=True
    ).annotate(
        product_count=Count('product', filter=Q(product__is_active=True))
    ).order_by('sort_order', 'name')[:15]  # Increased limit for more categories
    
    return {
        'global_categories': categories,
    }
