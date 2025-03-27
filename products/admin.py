# Register your models here.
from django.contrib import admin
from .models import Product, Category, Banner, Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    list_display = ('name', 'price', 'category', 'stock', 'is_featured')
    ist_editable = ('is_featured',) 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'is_active', 'created_at')
    list_filter = ('created_at', 'is_active')
    search_fields = ('title', 'subtitle', 'product__name')
    readonly_fields = ('created_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')