from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Wishlist

# View wishlist page
@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'products/wishlist.html', {'wishlist_items': wishlist_items})

# Add product to wishlist
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('products:wishlist')

# Remove product from wishlist
@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('products:wishlist')
# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count, F
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.core.cache import cache
import json

from .forms import BannerForm, ReviewForm 
from .models import Product, Category, Banner, Review, Brand, Wishlist, ProductView

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@cache_page(60 * 15)  # Cache for 15 minutes
def home(request):
    # Get active banners
    banners = Banner.objects.filter(is_active=True).select_related('product', 'category')
    active_banners = [banner for banner in banners if banner.is_active_now()]
    
    # Featured products with optimized queries
    featured_products = Product.objects.filter(
        is_featured=True, 
        is_active=True
    ).select_related('category', 'brand').prefetch_related('images')[:8]
    
    # Categories with product counts
    categories = Category.objects.filter(is_active=True).annotate(
        product_count=Count('product', filter=Q(product__is_active=True))
    ).order_by('sort_order')[:8]
    
    # Latest products
    latest_products = Product.objects.filter(is_active=True).select_related(
        'category', 'brand'
    ).order_by('-created_at')[:6]
    
    # Best selling products
    best_sellers = Product.objects.filter(is_active=True).select_related(
        'category', 'brand'
    ).order_by('-sales_count')[:6]
    
    # Top rated products
    top_rated = Product.objects.filter(
        is_active=True, 
        reviews__isnull=False
    ).annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(avg_rating__gte=4.0).order_by('-avg_rating', '-review_count')[:6]
    
    # Testimonials
    testimonials = Review.objects.filter(
        rating__gte=4, 
        is_approved=True
    ).select_related('user', 'product').order_by('-created_at')[:3]
    
    # Brands
    brands = Brand.objects.filter(is_active=True)[:8]
    
    # Get cart count (example: from session or user cart model)
    cart_count = 0
    if request.user.is_authenticated:
        try:
            from cart.models import Cart
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.items.count()
        except Exception:
            cart_count = 0
    context = {
        'banners': active_banners,
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products,
        'best_sellers': best_sellers,
        'top_rated': top_rated,
        'testimonials': testimonials,
        'brands': brands,
        'user': request.user,
        'cart_count': cart_count,
    }
    return render(request, 'products/home.html', context)

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related(
            'category', 'brand'
        ).prefetch_related('images')
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(short_description__icontains=query) |
                Q(tags__icontains=query)
            )
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Brand filter
        brand_slug = self.request.GET.get('brand')
        if brand_slug:
            queryset = queryset.filter(brand__slug=brand_slug)
        
        # Price range filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Sorting
        sort_by = self.request.GET.get('sort', 'name')
        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'popular':
            queryset = queryset.order_by('-sales_count')
        elif sort_by == 'rating':
            queryset = queryset.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        else:
            queryset = queryset.order_by('name')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['brands'] = Brand.objects.filter(is_active=True)
        context['current_category'] = self.request.GET.get('category')
        context['current_brand'] = self.request.GET.get('brand')
        context['current_sort'] = self.request.GET.get('sort', 'name')
        context['query'] = self.request.GET.get('q', '')
        context['user'] = self.request.user
        return context

def product_detail(request, slug=None, product_id=None):
    try:
        # Try to get by slug first, then by ID
        if slug:
            product = get_object_or_404(
                Product.objects.select_related('category', 'brand').prefetch_related(
                    'images', 'variants', 'reviews__user'
                ),
                slug=slug,
                is_active=True
            )
        elif product_id:
            product = get_object_or_404(
                Product.objects.select_related('category', 'brand').prefetch_related(
                    'images', 'variants', 'reviews__user'
                ),
                id=product_id,
                is_active=True
            )
        else:
            messages.error(request, "Product not found.")
            return redirect('products:product_list')
    except Http404:
        messages.error(request, "Product not found.")
        return redirect('products:product_list')
    
    # Track product view
    if not request.session.session_key:
        request.session.create()
    
    ProductView.objects.get_or_create(
        product=product,
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key,
        defaults={
            'ip_address': get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:255]
        }
    )
    
    # Increment views count
    Product.objects.filter(id=product.id).update(views_count=F('views_count') + 1)
    
    # Related products
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).select_related('category', 'brand')[:4]
    
    # Recently viewed products (from cache)
    recently_viewed = []
    if request.user.is_authenticated:
        cache_key = f"recently_viewed_{request.user.id}"
        recently_viewed_ids = cache.get(cache_key, [])
        if product.id not in recently_viewed_ids:
            recently_viewed_ids.insert(0, product.id)
            recently_viewed_ids = recently_viewed_ids[:10]  # Keep last 10
            cache.set(cache_key, recently_viewed_ids, 60 * 60 * 24)  # 24 hours
        
        if len(recently_viewed_ids) > 1:
            recently_viewed = Product.objects.filter(
                id__in=recently_viewed_ids[1:],  # Exclude current product
                is_active=True
            )[:4]
    
    # Check if in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).exists()
    
    # Review form
    review_form = ReviewForm()
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review, created = Review.objects.get_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': review_form.cleaned_data['rating'],
                    'title': review_form.cleaned_data['title'],
                    'comment': review_form.cleaned_data['comment'],
                }
            )
            if not created:
                review.rating = review_form.cleaned_data['rating']
                review.title = review_form.cleaned_data['title']
                review.comment = review_form.cleaned_data['comment']
                review.save()
                messages.success(request, "Your review has been updated.")
            else:
                messages.success(request, "Thank you for your review!")
            return redirect('products:product_detail', product_id=product.slug or product.id)
    
    context = {
        'product': product,
        'related_products': related_products,
        'recently_viewed': recently_viewed,
        'in_wishlist': in_wishlist,
        'review_form': review_form,
    }
    return render(request, 'products/enhanced_product_detail.html', context)

@login_required
def toggle_wishlist(request, product_id):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, id=product_id, is_active=True)
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user,
                product=product
            )
            
            if not created:
                wishlist_item.delete()
                in_wishlist = False
                message = "Removed from wishlist"
            else:
                in_wishlist = True
                message = "Added to wishlist"
            
            return JsonResponse({
                'success': True,
                'in_wishlist': in_wishlist,
                'message': message
            })
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Product not found'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related(
        'product__category', 'product__brand'
    ).order_by('-created_at')
    
    paginator = Paginator(wishlist_items, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'wishlist_items': page_obj,
        'total_items': wishlist_items.count()
    }
    return render(request, 'products/wishlist.html', context)

def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    
    products = Product.objects.filter(
        category=category,
        is_active=True
    ).select_related('brand').prefetch_related('images')
    
    # Apply filters and sorting (same as ProductListView)
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'popular':
        products = products.order_by('-sales_count')
    else:
        products = products.order_by('name')
    
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': page_obj,
        'current_sort': sort_by,
        'query': query,
    }
    return render(request, 'products/category_detail.html', context)

def search_suggestions(request):
    """AJAX endpoint for search autocomplete"""
    query = request.GET.get('q', '').strip()
    suggestions = []
    
    if len(query) >= 2:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(tags__icontains=query),
            is_active=True
        ).values('name', 'slug', 'id')[:10]
        
        suggestions = [
            {
                'name': product['name'],
                'url': f"/products/{product['slug'] or product['id']}/"
            }
            for product in products
        ]
    
    return JsonResponse({'suggestions': suggestions})

def upload_banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Banner uploaded successfully!")
            return redirect('products:home')
    else:
        form = BannerForm()
    
    return render(request, 'products/upload_banner.html', {'form': form})

# Special product views
def featured_products(request):
    """Display featured products"""
    products = Product.objects.filter(is_featured=True, is_active=True)[:12]
    context = {
        'products': products,
        'page_title': 'Featured Products',
        'page_description': 'Discover our hand-picked featured products'
    }
    return render(request, 'products/product_list.html', context)

def deals(request):
    """Display products on deal/sale"""
    products = Product.objects.filter(
        discount_percentage__gt=0, 
        is_active=True
    ).order_by('-discount_percentage')[:20]
    context = {
        'products': products,
        'page_title': "Today's Deals",
        'page_description': 'Amazing deals and discounts on selected products'
    }
    return render(request, 'products/product_list.html', context)

def new_arrivals(request):
    """Display new arrival products"""
    products = Product.objects.filter(
        is_active=True
    ).order_by('-created_at')[:16]
    context = {
        'products': products,
        'page_title': 'New Arrivals',
        'page_description': 'Check out our latest products'
    }
    return render(request, 'products/product_list.html', context)

def bestsellers(request):
    """Display bestselling products"""
    products = Product.objects.filter(
        is_active=True
    ).order_by('-view_count')[:16]
    context = {
        'products': products,
        'page_title': 'Bestsellers',
        'page_description': 'Our most popular products'
    }
    return render(request, 'products/product_list.html', context)

def sale_products(request):
    """Display products on sale"""
    products = Product.objects.filter(
        discount_percentage__gt=0,
        is_active=True
    ).order_by('-discount_percentage')
    context = {
        'products': products,
        'page_title': 'Sale Products',
        'page_description': 'Great savings on quality products'
    }
    return render(request, 'products/product_list.html', context)

# Customer service views
def contact(request):
    """Contact us page"""
    context = {
        'page_title': 'Contact Us',
        'page_description': 'Get in touch with Riya Group customer service'
    }
    return render(request, 'products/contact.html', context)

def faq(request):
    """Frequently Asked Questions page"""
    context = {
        'page_title': 'Frequently Asked Questions',
        'page_description': 'Find answers to common questions'
    }
    return render(request, 'products/faq.html', context)

def customer_support(request):
    """Customer support page"""
    context = {
        'page_title': 'Customer Support',
        'page_description': '24/7 customer support for Riya Group'
    }
    return render(request, 'products/support.html', context)

def shipping_info(request):
    """Shipping information page"""
    context = {
        'page_title': 'Shipping Information',
        'page_description': 'Learn about our shipping policies and delivery options'
    }
    return render(request, 'products/shipping.html', context)

def returns_policy(request):
    """Returns policy page"""
    context = {
        'page_title': 'Returns Policy',
        'page_description': 'Easy returns and refunds at Riya Group'
    }
    return render(request, 'products/returns.html', context)

def size_guide(request):
    """Size guide page"""
    context = {
        'page_title': 'Size Guide',
        'page_description': 'Find the perfect fit with our size guide'
    }
    return render(request, 'products/size_guide.html', context)

def track_order(request):
    """Order tracking page"""
    context = {
        'page_title': 'Track Your Order',
        'page_description': 'Track your Riya Group order in real-time'
    }
    return render(request, 'products/track_order.html', context)

# Legal pages
def privacy_policy(request):
    """Privacy policy page"""
    context = {
        'page_title': 'Privacy Policy',
        'page_description': 'Your privacy is important to us'
    }
    return render(request, 'products/privacy.html', context)

def terms_of_service(request):
    """Terms of service page"""
    context = {
        'page_title': 'Terms of Service',
        'page_description': 'Terms and conditions for using Riya Group'
    }
    return render(request, 'products/terms.html', context)

def cookies_policy(request):
    """Cookies policy page"""
    context = {
        'page_title': 'Cookies Policy',
        'page_description': 'How we use cookies to improve your experience'
    }
    return render(request, 'products/cookies.html', context)

# Special services
def gift_cards(request):
    """Gift cards page"""
    context = {
        'page_title': 'Gift Cards',
        'page_description': 'Give the gift of choice with Riya Group gift cards'
    }
    return render(request, 'products/gift_cards.html', context)

def prime_membership(request):
    """Prime membership page"""
    context = {
        'page_title': 'Riya Group Prime',
        'page_description': 'Exclusive benefits for Prime members'
    }
    return render(request, 'products/prime.html', context)