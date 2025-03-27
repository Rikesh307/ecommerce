from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

# products/models.py
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False)  # Add this line
    
    def __str__(self):
        return self.name

class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(
    upload_to='banners/',
    help_text="Recommended size: 1920x1080 pixels"  # This is the key change
    )
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    subtitle = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"