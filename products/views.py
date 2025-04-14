"""
from django.shortcuts import render
from .models import Product  # Import your Product model

def product_list(request):
    products = Product.objects.all()  # Fetch all products from DB
    return render(request, 'products/product_list.html', {'products': products})"
"""
# products/viwes.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BannerForm 
from .models import Product, Category, Banner, Review

def home(request):
    context = {
        'banners': Banner.objects.filter(is_active=True),
        'featured_products': Product.objects.filter(is_featured=True)[:6],
        'categories': Category.objects.all(),
        'testimonials': Review.objects.filter(rating=5)[:3],
    }
    return render(request, 'products/home.html', context) 

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

def upload_banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to your home page
    else:
        form = BannerForm()
    
    return render(request, 'products/upload_banner.html', {'form': form})