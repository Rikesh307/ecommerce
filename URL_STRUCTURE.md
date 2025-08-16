# E-Commerce Website URL Structure

## Main URLs (ecommerce/urls.py)
- `/` - Homepage (home view)
- `/admin/` - Django Admin Panel
- `/accounts/` - User Authentication URLs
- `/cart/` - Shopping Cart URLs  
- `/orders/` - Order Management URLs
- `/products/` - Product Catalog URLs

## User Authentication URLs (accounts/urls.py)
**App Name: accounts**
- `/accounts/login/` - Login page (`accounts:login`)
- `/accounts/logout/` - Logout (`accounts:logout`)
- `/accounts/register/` - Registration page (`accounts:register`)
- `/accounts/profile/` - User profile (`accounts:profile`)

## Product URLs (products/urls.py)  
**App Name: products**
- `/products/` - Product list (`products:product_list`)
- `/products/<id>/` - Product detail (`products:product_detail`)
- `/products/upload-banner/` - Banner upload (`products:upload_banner`)

## Shopping Cart URLs (cart/urls.py)
**App Name: cart**
- `/cart/` - Cart details (`cart:cart_detail`)
- `/cart/add/<id>/` - Add to cart (`cart:add_to_cart`)
- `/cart/update/` - Update cart item (`cart:update_cart`)
- `/cart/remove/` - Remove from cart (`cart:remove_from_cart`)

## Order URLs (orders/urls.py)
**App Name: orders**
- `/orders/checkout/` - Checkout page (`orders:checkout`)
- `/orders/create-payment-intent/` - Stripe payment intent (`orders:create_payment_intent`)
- `/orders/process-payment/` - Process payment (`orders:process_payment`)
- `/orders/success/<id>/` - Order success (`orders:order_success`)
- `/orders/history/` - Order history (`orders:order_history`)

## Template URL Usage
All templates should use namespaced URLs:
```django
<!-- Correct -->
{% url 'accounts:login' %}
{% url 'products:product_detail' product.id %}
{% url 'cart:cart_detail' %}

<!-- Incorrect (will cause errors) -->
{% url 'login' %}
{% url 'product_detail' product.id %}
{% url 'cart_detail' %}
```

## Navigation Links
The main navigation includes:
- **Desktop**: Dropdown menu in header with authentication links
- **Mobile**: Bottom navigation bar for small screens
- **Dynamic**: Shows different options for logged-in vs anonymous users

## Status: ✅ All URLs Working
- All URL patterns properly configured with app names
- All templates use correct namespaced URLs
- Navigation links working on both desktop and mobile
- No reverse match errors
