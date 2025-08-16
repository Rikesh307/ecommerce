# products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Main product views
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail_by_id'),
    path('category/<slug:category_slug>/', views.category_detail, name='category'),
    
    # Special product pages
    path('featured/', views.featured_products, name='featured'),
    path('deals/', views.deals, name='deals'),
    path('new-arrivals/', views.new_arrivals, name='new_arrivals'),
    path('bestsellers/', views.bestsellers, name='bestsellers'),
    path('sale/', views.sale_products, name='sale'),
    
    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    
    # Customer service pages
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('support/', views.customer_support, name='support'),
    path('shipping/', views.shipping_info, name='shipping'),
    path('returns/', views.returns_policy, name='returns'),
    path('size-guide/', views.size_guide, name='size_guide'),
    path('track-order/', views.track_order, name='track_order'),
    
    # Legal pages
    path('privacy/', views.privacy_policy, name='privacy'),
    path('terms/', views.terms_of_service, name='terms'),
    path('cookies/', views.cookies_policy, name='cookies'),
    
    # Special services
    path('gift-cards/', views.gift_cards, name='gift_cards'),
    path('prime/', views.prime_membership, name='prime'),
    
    # AJAX endpoints
    path('api/search-suggestions/', views.search_suggestions, name='search_suggestions'),
    
    # Admin functions
    path('upload-banner/', views.upload_banner, name='upload_banner'),
]