# Website Sitemap - Riya Group E-commerce

## Current Pages Available:

### 🏠 Homepage (/)
- **URL**: http://127.0.0.1:8000/
- **Features**: 
  - Dynamic banner carousel
  - Featured products section
  - Categories display
  - Responsive sky-blue header

### 🛒 Products (/products/)
- **URL**: http://127.0.0.1:8000/products/
- **Features**:
  - Product grid layout
  - Product filtering (ready for enhancement)
  - Category-based organization

### 📱 Product Detail (/products/<id>/)
- **Example**: http://127.0.0.1:8000/products/1/
- **Features**:
  - Product images
  - Detailed descriptions
  - Pricing information
  - Stock status

### 🔧 Admin Panel (/admin/)
- **URL**: http://127.0.0.1:8000/admin/
- **Features**:
  - Product management
  - Category management
  - Banner management
  - User administration

### 📤 Upload Banner (/products/upload-banner/)
- **URL**: http://127.0.0.1:8000/products/upload-banner/
- **Features**:
  - Banner upload form
  - Image handling
  - Product association

## 🔜 Future Pages (Ready to Implement):

### User Authentication:
- `/accounts/login/` - User login
- `/accounts/register/` - User registration
- `/accounts/profile/` - User profile
- `/accounts/logout/` - User logout

### Shopping Cart:
- `/cart/` - Shopping cart
- `/cart/add/<product_id>/` - Add to cart
- `/checkout/` - Checkout process

### Search & Navigation:
- `/search/` - Search results
- `/categories/<slug>/` - Category pages
- `/products/featured/` - Featured products

### User Features:
- `/wishlist/` - User wishlist
- `/orders/` - Order history
- `/reviews/` - Product reviews

## 📊 Database Models:

### Product Model:
- Name, price, description
- Image upload
- Stock management
- Category association
- Featured flag

### Category Model:
- Name and slug
- Description
- SEO-friendly URLs

### Banner Model:
- Title and subtitle
- Image upload
- Product association
- Active/inactive status

### Review Model:
- User reviews
- Rating system
- Product association

## 🎨 Design Features:

### Color Scheme:
- **Primary**: Sky Blue (#87CEEB)
- **Secondary**: Steel Blue (#4682B4)
- **Accent**: Light Blue (#B0E0E6)

### Layout Features:
- Responsive Bootstrap 5 design
- Fixed header with proper alignment
- Mobile-friendly navigation
- Professional product cards
- Smooth carousel transitions

## 🚀 Quick Navigation Commands:

```bash
# Start development server
python manage.py runserver

# Access admin panel
# URL: http://127.0.0.1:8000/admin/
# Username: rikesh
# Password: [your_password]

# Load sample data
python manage.py load_sample_data

# Create new superuser
python manage.py createsuperuser
```

---
*This sitemap reflects the current state of your Django e-commerce project.*
