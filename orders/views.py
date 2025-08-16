from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from .models import Order, OrderItem
from cart.models import Cart
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    """Display checkout page"""
    # Ensure CSRF token is set in cookies
    get_token(request)
    
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.warning(request, 'Your cart is empty!')
            return redirect('cart:cart_detail')
    except Cart.DoesNotExist:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart:cart_detail')
    
    cart_items = cart.items.all()
    cart_total = cart.total_price
    
    # Ensure CSRF token is set
    csrf_token = get_token(request)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
        'csrf_token': csrf_token
    }
    return render(request, 'orders/checkout.html', context)


@login_required
@require_POST
def create_payment_intent(request):
    """Create Stripe payment intent"""
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            return JsonResponse({'error': 'Cart is empty'}, status=400)
            
        amount = int(cart.total_price * 100)  # Convert to cents
        
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            metadata={
                'user_id': request.user.id,
                'cart_id': cart.id
            }
        )
        
        return JsonResponse({
            'client_secret': intent.client_secret
        })
        
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart not found'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_POST
def process_payment(request):
    """Process successful payment and create order"""
    try:
        data = json.loads(request.body)
        cart = Cart.objects.get(user=request.user)
        
        if not cart.items.exists():
            return JsonResponse({'error': 'Cart is empty'}, status=400)
        
        # Verify payment intent with Stripe
        payment_intent_id = data['payment_intent_id']
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if intent.status != 'succeeded':
                return JsonResponse({'error': 'Payment not completed'}, status=400)
        except stripe.error.StripeError as e:
            return JsonResponse({'error': f'Payment verification failed: {str(e)}'}, status=400)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            zip_code=data['zip_code'],
            stripe_payment_intent_id=payment_intent_id,
            payment_status='completed',
            status='processing'
        )
        
        # Create order items and update stock
        for cart_item in cart.items.all():
            # Check if product still has enough stock
            if cart_item.product.stock < cart_item.quantity:
                # Delete the order and return error
                order.delete()
                return JsonResponse({
                    'error': f'Not enough stock for {cart_item.product.name}. Only {cart_item.product.stock} available.'
                }, status=400)
            
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Update product stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart.items.all().delete()
        
        # Clear cart count from session
        request.session['cart_count'] = 0
        
        return JsonResponse({
            'success': True,
            'redirect_url': f'/orders/success/{order.id}/'
        })
        
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart not found'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def order_success(request, order_id):
    """Display order success page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history(request):
    """Display order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})
