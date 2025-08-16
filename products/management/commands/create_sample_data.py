from django.core.management.base import BaseCommand
from products.models import Category, Product, Brand
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Create sample categories and products for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample categories and products...')
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Fashion', 'description': 'Clothing and accessories'},
            {'name': 'Home & Garden', 'description': 'Home and garden products'},
            {'name': 'Books', 'description': 'Books and educational materials'},
            {'name': 'Sports', 'description': 'Sports and fitness equipment'},
            {'name': 'Beauty', 'description': 'Beauty and personal care'},
            {'name': 'Automotive', 'description': 'Automotive parts and accessories'},
            {'name': 'Toys', 'description': 'Toys and games'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description'],
                    'is_active': True,
                    'sort_order': len(categories)
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')
        
        # Create brands
        brands_data = [
            'Samsung', 'Apple', 'Nike', 'Adidas', 'Sony', 'LG', 'HP', 'Dell',
            'Canon', 'Nikon', 'Asus', 'Lenovo', 'Xiaomi', 'OnePlus'
        ]
        
        brands = []
        for brand_name in brands_data:
            brand, created = Brand.objects.get_or_create(
                name=brand_name,
                defaults={
                    'slug': slugify(brand_name),
                    'is_active': True
                }
            )
            brands.append(brand)
            if created:
                self.stdout.write(f'Created brand: {brand.name}')
            else:
                self.stdout.write(f'Brand already exists: {brand.name}')
        
        # Create sample products
        products_data = [
            {
                'name': 'Samsung Galaxy S24',
                'category': 'Electronics',
                'brand': 'Samsung',
                'price': 999.99,
                'description': 'Latest Samsung flagship smartphone with advanced camera features.',
                'short_description': 'Premium smartphone with excellent camera and performance.'
            },
            {
                'name': 'Nike Air Max 270',
                'category': 'Fashion',
                'brand': 'Nike',
                'price': 129.99,
                'description': 'Comfortable and stylish sneakers for everyday wear.',
                'short_description': 'Stylish and comfortable sneakers for all occasions.'
            },
            {
                'name': 'Dell XPS 13 Laptop',
                'category': 'Electronics',
                'brand': 'Dell',
                'price': 1299.99,
                'description': 'Powerful ultrabook perfect for work and entertainment.',
                'short_description': 'High-performance laptop with stunning display.'
            },
            {
                'name': 'Adidas Ultraboost 22',
                'category': 'Sports',
                'brand': 'Adidas',
                'price': 189.99,
                'description': 'Premium running shoes with responsive cushioning.',
                'short_description': 'Advanced running shoes for serious athletes.'
            },
            {
                'name': 'Apple MacBook Air M2',
                'category': 'Electronics',
                'brand': 'Apple',
                'price': 1199.99,
                'description': 'Revolutionary laptop with Apple M2 chip for incredible performance.',
                'short_description': 'Powerful and efficient laptop with M2 chip.'
            },
        ]
        
        for product_data in products_data:
            # Get category and brand
            try:
                category = Category.objects.get(name=product_data['category'])
                brand = Brand.objects.get(name=product_data['brand'])
                
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        'slug': slugify(product_data['name']),
                        'category': category,
                        'brand': brand,
                        'price': product_data['price'],
                        'description': product_data['description'],
                        'short_description': product_data['short_description'],
                        'is_active': True,
                        'is_featured': True,
                        'stock': 50,
                        'condition': 'new'
                    }
                )
                
                if created:
                    self.stdout.write(f'Created product: {product.name}')
                else:
                    self.stdout.write(f'Product already exists: {product.name}')
                    
            except (Category.DoesNotExist, Brand.DoesNotExist) as e:
                self.stdout.write(f'Error creating product {product_data["name"]}: {e}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
