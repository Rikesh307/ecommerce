from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('success/<uuid:order_id>/', views.order_success, name='order_success'),
    path('history/', views.order_history, name='order_history'),
]
