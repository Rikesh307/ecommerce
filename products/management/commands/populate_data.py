from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Brand, Product, Banner, ProductImage
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics', 'description': 'Latest electronic gadgets and devices'},
            {'name': 'Clothing', 'slug': 'clothing', 'description': 'Fashion and apparel for everyone'},
            {'name': 'Home & Garden', 'slug': 'home-garden', 'description': 'Everything for your home and garden'},
            {'name': 'Sports', 'slug': 'sports', 'description': 'Sports equipment and gear'},
            {'name': 'Books', 'slug': 'books', 'description': 'Books and educational materials'},
        ]
        
        created_categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(**cat_data)
            if created:
                created_categories.append(category)
                self.stdout.write(f'Created category: {category.name}')
        
        # Create brands
        brands_data = [
            {'name': 'Samsung', 'slug': 'samsung'},
            {'name': 'Apple', 'slug': 'apple'},
            {'name': 'Nike', 'slug': 'nike'},
            {'name': 'Adidas', 'slug': 'adidas'},
            {'name': 'Sony', 'slug': 'sony'},
        ]
        
        created_brands = []
        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(**brand_data)
            if created:
                created_brands.append(brand)
                self.stdout.write(f'Created brand: {brand.name}')
        
        # Create products
        if created_categories and created_brands:
            products_data = [
                {
                    'name': 'Samsung Galaxy S23',
                    'slug': 'samsung-galaxy-s23',
                    'description': 'Latest Samsung Galaxy smartphone with amazing features',
                    'short_description': 'Premium smartphone with excellent camera',
                    'price': Decimal('999.99'),
                    'compare_price': Decimal('1199.99'),
                    'stock': 50,
                    'category': created_categories[0],  # Electronics
                    'brand': created_brands[0],  # Samsung
                    'is_featured': True,
                },
                {
                    'name': 'iPhone 15 Pro',
                    'slug': 'iphone-15-pro',
                    'description': 'Apple iPhone 15 Pro with titanium design and A17 Pro chip',
                    'short_description': 'Flagship iPhone with pro camera system',
                    'price': Decimal('1299.99'),
                    'compare_price': Decimal('1399.99'),
                    'stock': 30,
                    'category': created_categories[0],  # Electronics
                    'brand': created_brands[1],  # Apple
                    'is_featured': True,
                },
                {
                    'name': 'Nike Air Max 270',
                    'slug': 'nike-air-max-270',
                    'description': 'Comfortable running shoes with air cushioning technology',
                    'short_description': 'Premium running shoes for athletes',
                    'price': Decimal('150.00'),
                    'compare_price': Decimal('180.00'),
                    'stock': 100,
                    'category': created_categories[3],  # Sports
                    'brand': created_brands[2],  # Nike
                    'is_featured': False,
                },
                {
                    'name': 'Sony WH-1000XM5',
                    'slug': 'sony-wh-1000xm5',
                    'description': 'Premium noise-canceling wireless headphones',
                    'short_description': 'Industry-leading noise cancellation',
                    'price': Decimal('399.99'),
                    'stock': 25,
                    'category': created_categories[0],  # Electronics
                    'brand': created_brands[4],  # Sony
                    'is_featured': True,
                },
            ]
            
            for product_data in products_data:
                product, created = Product.objects.get_or_create(
                    slug=product_data['slug'],
                    defaults=product_data
                )
                if created:
                    self.stdout.write(f'Created product: {product.name}')
        
        # Create a banner
        if Product.objects.exists():
            featured_product = Product.objects.filter(is_featured=True).first()
            banner_data = {
                'title': 'Summer Sale',
                'subtitle': 'Up to 50% off on selected items',
                'product': featured_product,
                'cta_text': 'Shop Now',
                'cta_style': 'warning',
                'is_active': True,
            }
            
            banner, created = Banner.objects.get_or_create(
                title=banner_data['title'],
                defaults=banner_data
            )
            if created:
                self.stdout.write(f'Created banner: {banner.title}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
