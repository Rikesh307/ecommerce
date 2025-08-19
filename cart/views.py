from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from products.models import Product
import json


# Constants
JSON_CONTENT_TYPE = 'application/json'
PRODUCT_DETAIL_URL = 'products:product_detail'


@login_required
def cart_detail(request):
    """Display cart contents"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    cart_total = cart.total_price
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart': cart,
        'user': request.user,
    }
    return render(request, 'cart/cart.html', context)


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is in stock
    if product.stock <= 0:
        if request.content_type == JSON_CONTENT_TYPE:
            return JsonResponse({
                'success': False,
                'error': 'Product is out of stock'
            })
        messages.error(request, 'Product is out of stock')
        return redirect(PRODUCT_DETAIL_URL, product_id=product.id)
    
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    # Get quantity from request
    quantity = 1
    if request.content_type == JSON_CONTENT_TYPE:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
    
    # Check if adding this quantity would exceed stock
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    current_quantity = cart_item.quantity if cart_item else 0
    
    if current_quantity + quantity > product.stock:
        if request.content_type == JSON_CONTENT_TYPE:
            return JsonResponse({
                'success': False,
                'error': f'Only {product.stock - current_quantity} items available'
            })
        messages.error(request, f'Only {product.stock - current_quantity} items available')
        return redirect(PRODUCT_DETAIL_URL, product_id=product.id)
    
    # Add to cart
    if cart_item:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
    
    # Update session cart count
    request.session['cart_count'] = cart.total_items
    
    if request.content_type == JSON_CONTENT_TYPE:
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'cart_total': float(cart.total_price),
            'message': f'{product.name} added to cart!'
        })
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect(PRODUCT_DETAIL_URL, product_id=product.id)


@login_required
@require_POST
def update_cart(request):
    """Update cart item quantity via AJAX"""
    if request.content_type != JSON_CONTENT_TYPE:
        return JsonResponse({'success': False, 'error': 'Invalid request'})
    
    data = json.loads(request.body)
    item_id = data.get('item_id')
    quantity = int(data.get('quantity', 1))
    
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    # Check stock availability
    if quantity > cart_item.product.stock:
        return JsonResponse({
            'success': False,
            'error': f'Only {cart_item.product.stock} items available'
        })
    
    if quantity <= 0:
        return JsonResponse({
            'success': False,
            'error': 'Quantity must be at least 1'
        })
    
    cart_item.quantity = quantity
    cart_item.save()
    
    # Update session cart count
    request.session['cart_count'] = cart_item.cart.total_items
    
    return JsonResponse({
        'success': True,
        'item_total': float(cart_item.get_total_price()),
        'cart_total': float(cart_item.cart.total_price),
        'cart_count': cart_item.cart.total_items
    })


@login_required
@require_POST
def remove_from_cart(request):
    """Remove item from cart via AJAX"""
    if request.content_type != JSON_CONTENT_TYPE:
        return JsonResponse({'success': False, 'error': 'Invalid request'})
    
    data = json.loads(request.body)
    item_id = data.get('item_id')
    
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart = cart_item.cart
    cart_item.delete()
    
    # Update session cart count
    request.session['cart_count'] = cart.total_items
    
    return JsonResponse({
        'success': True,
        'cart_total': float(cart.total_price),
        'cart_count': cart.total_items,
        'message': f'{product_name} removed from cart!'
    })
