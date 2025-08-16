from .models import Cart


def cart_context(request):
    """Add cart context to all templates"""
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.total_items
        except Cart.DoesNotExist:
            cart_count = 0
    
    # Update session
    request.session['cart_count'] = cart_count
    
    return {
        'cart_count': cart_count,
    }
