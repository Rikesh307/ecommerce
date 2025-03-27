"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
]
"""
# products/urls.py
from django.urls import path
from . import views
from .views import upload_banner

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('upload-banner/', upload_banner, name='upload_banner'),
    
]