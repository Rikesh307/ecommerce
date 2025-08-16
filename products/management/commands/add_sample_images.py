from django.core.management.base import BaseCommand
from products.models import Product, Banner


class Command(BaseCommand):
    help = 'Display instructions for adding images to products and banners'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Image Upload Instructions ==='))
        self.stdout.write('')
        
        self.stdout.write(self.style.WARNING('To add images to your products and banners:'))
        self.stdout.write('')
        
        self.stdout.write('1. 📱 Access Admin Panel:')
        self.stdout.write('   Visit: http://127.0.0.1:8000/admin/')
        self.stdout.write('   Login with your superuser credentials')
        self.stdout.write('')
        
        self.stdout.write('2. 🛍️ Add Product Images:')
        self.stdout.write('   - Go to "Products" section')
        self.stdout.write('   - Click on any product to edit')
        self.stdout.write('   - Use the "Image" field to upload product photos')
        self.stdout.write('   - Recommended size: 400x400 pixels')
        self.stdout.write('')
        
        self.stdout.write('3. 🏞️ Add Banner Images:')
        self.stdout.write('   - Go to "Banners" section')
        self.stdout.write('   - Click on any banner to edit')
        self.stdout.write('   - Use the "Image" field to upload banner photos')
        self.stdout.write('   - Recommended size: 1920x1080 pixels (16:9 ratio)')
        self.stdout.write('')
        
        self.stdout.write('4. 📂 Alternative Upload Methods:')
        self.stdout.write('   - Use the banner upload form: http://127.0.0.1:8000/products/upload-banner/')
        self.stdout.write('   - Copy images to the media/ folder and reference them')
        self.stdout.write('')
        
        # Show current status
        products_without_images = Product.objects.filter(image='').count() + Product.objects.filter(image__isnull=True).count()
        products_with_images = Product.objects.exclude(image='').exclude(image__isnull=True).count()
        banners_without_images = Banner.objects.filter(image='').count() + Banner.objects.filter(image__isnull=True).count()
        banners_with_images = Banner.objects.exclude(image='').exclude(image__isnull=True).count()
        
        self.stdout.write(self.style.SUCCESS('📊 Current Status:'))
        self.stdout.write(f'   Products with images: {products_with_images}')
        self.stdout.write(f'   Products without images: {products_without_images}')
        self.stdout.write(f'   Banners with images: {banners_with_images}')
        self.stdout.write(f'   Banners without images: {banners_without_images}')
        self.stdout.write('')
        
        if products_without_images > 0 or banners_without_images > 0:
            self.stdout.write(self.style.WARNING('💡 Note: Products and banners without images will show placeholder icons.'))
            self.stdout.write('    The website is fully functional, but adding images will make it look more professional!')
        else:
            self.stdout.write(self.style.SUCCESS('🎉 All products and banners have images!'))
            
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Happy shopping! 🛒'))
