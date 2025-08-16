from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Banner, Review, Product, Category, Brand

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'subtitle', 'image', 'mobile_image', 'product', 'category', 
                 'external_url', 'cta_text', 'cta_style', 'is_active', 'show_on_mobile', 
                 'start_date', 'end_date', 'sort_order']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter banner title'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter short description'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'mobile_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'product': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'external_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'cta_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Shop Now'
            }),
            'cta_style': forms.Select(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'sort_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = "Recommended size: 1920x1080 pixels (16:9 ratio)"
        self.fields['mobile_image'].help_text = "Recommended size: 750x1334 pixels (mobile optimized)"
        self.fields['subtitle'].required = False
        self.fields['product'].required = False
        self.fields['category'].required = False
        self.fields['external_url'].required = False
        self.fields['end_date'].required = False

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Summary of your review'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this product...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False

class ProductSearchForm(forms.Form):
    q = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search products...',
            'autocomplete': 'off'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.filter(is_active=True),
        required=False,
        empty_label="All Brands",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Price',
            'step': '0.01'
        })
    )
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Price',
            'step': '0.01'
        })
    )
    sort = forms.ChoiceField(
        choices=[
            ('name', 'Name A-Z'),
            ('price_low', 'Price: Low to High'),
            ('price_high', 'Price: High to Low'),
            ('newest', 'Newest First'),
            ('popular', 'Most Popular'),
            ('rating', 'Highest Rated'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ProductFilterForm(forms.Form):
    """Advanced product filtering form"""
    CONDITION_CHOICES = [
        ('', 'Any Condition'),
        ('new', 'New'),
        ('refurbished', 'Refurbished'),
        ('used', 'Used'),
    ]
    
    AVAILABILITY_CHOICES = [
        ('', 'All Products'),
        ('in_stock', 'In Stock'),
        ('on_sale', 'On Sale'),
        ('featured', 'Featured'),
    ]
    
    condition = forms.ChoiceField(
        choices=CONDITION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    availability = forms.ChoiceField(
        choices=AVAILABILITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    rating = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.Select(
            choices=[('', 'Any Rating')] + [(i, f'{i}+ Stars') for i in range(1, 6)],
            attrs={'class': 'form-control'}
        )
    )