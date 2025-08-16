from django.core.management.base import BaseCommand
from products.models import Category, Product, Banner
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Load sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'slug': 'clothing', 'description': 'Fashion and clothing items'},
            {'name': 'Home & Garden', 'slug': 'home-garden', 'description': 'Home and garden products'},
            {'name': 'Sports', 'slug': 'sports', 'description': 'Sports and fitness equipment'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create products
        electronics = Category.objects.get(slug='electronics')
        clothing = Category.objects.get(slug='clothing')
        home_garden = Category.objects.get(slug='home-garden')
        
        products_data = [
            {
                'name': '4K Smart TV',
                'price': 599.99,
                'description': 'Ultra HD 4K Smart TV with HDR support and streaming apps',
                'stock': 25,
                'category': electronics,
                'is_featured': True
            },
            {
                'name': 'Gaming Laptop',
                'price': 1299.99,
                'description': 'High-performance gaming laptop with RTX graphics',
                'stock': 15,
                'category': electronics,
                'is_featured': True
            },
            {
                'name': 'Wireless Headphones',
                'price': 199.99,
                'description': 'Premium wireless headphones with noise cancellation',
                'stock': 50,
                'category': electronics,
                'is_featured': False
            },
            {
                'name': 'Summer T-Shirt',
                'price': 29.99,
                'description': 'Comfortable cotton t-shirt perfect for summer',
                'stock': 100,
                'category': clothing,
                'is_featured': True
            },
            {
                'name': 'Designer Jeans',
                'price': 89.99,
                'description': 'Premium designer jeans with perfect fit',
                'stock': 75,
                'category': clothing,
                'is_featured': False
            },
            {
                'name': 'Coffee Maker',
                'price': 149.99,
                'description': 'Programmable coffee maker with 12-cup capacity',
                'stock': 30,
                'category': home_garden,
                'is_featured': True
            }
        ]
        
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults=prod_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        # Create banners for featured products (without images for now)
        featured_products = Product.objects.filter(is_featured=True)[:3]
        
        banner_data = [
            {
                'title': 'Latest 4K Technology',
                'subtitle': 'Experience cinema-quality viewing at home with our premium 4K Smart TVs',
                'is_active': True
            },
            {
                'title': 'Gaming Revolution',
                'subtitle': 'Unleash your gaming potential with our high-performance laptops',
                'is_active': True
            },
            {
                'title': 'Summer Collection',
                'subtitle': 'Stay cool and stylish with our latest summer apparel',
                'is_active': True
            }
        ]
        
        # Delete existing banners to avoid duplicates
        Banner.objects.all().delete()
        
        for i, banner_info in enumerate(banner_data):
            if i < len(featured_products):
                banner = Banner.objects.create(
                    title=banner_info['title'],
                    subtitle=banner_info['subtitle'],
                    product=featured_products[i],
                    is_active=banner_info['is_active']
                    # Note: No image field - will use gradient background
                )
                self.stdout.write(f'Created banner: {banner.title}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
