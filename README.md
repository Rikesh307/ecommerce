# Django E-commerce Project

A modern, full-featured e-commerce website built with Django, featuring a beautiful sky-blue themed interface, complete user authentication, shopping cart functionality, and Stripe payment integration.

## 🚀 Features

### ✅ **Complete E-commerce Functionality**
- **User Authentication**: Full registration, login, logout, and profile management
- **Shopping Cart**: Add to cart, update quantities, remove items with AJAX
- **Order Management**: Complete checkout process with order history
- **Payment Processing**: Secure Stripe payment integration
- **Product Catalog**: Browse, search, and view product details

### 🎨 **Modern UI & UX**
- **Beautiful Interface**: Sky-blue themed design with gradients and animations
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Professional Header**: Modern navigation with cart counter and user menu
- **Interactive Cart**: Real-time updates without page reloads
- **Smooth Checkout**: Clean, secure payment flow

### 🛠️ **Technical Features**
- **AJAX Integration**: Seamless user experience
- **Session Management**: Cart persistence across browser sessions
- **Image Handling**: Product images with graceful fallbacks
- **Context Processors**: Global cart count availability
- **Form Validation**: Crispy forms with Bootstrap styling

## 🛠️ Technology Stack

- **Backend**: Django 5.2
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Image Handling**: Pillow
- **Icons**: Bootstrap Icons

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Quick Start

1. **Clone or navigate to your project directory**
   ```bash
   cd c:\Users\rikes\ecommerce
   ```

2. **Activate virtual environment**
   ```bash
   # Windows
   env\Scripts\activate
   
   # Linux/Mac
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Load sample data**
   ```bash
   python manage.py load_sample_data
   ```

6. **Create superuser (if not already created)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Visit your site**
   - Website: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

### Alternative: Use Build Scripts

**Windows PowerShell:**
```powershell
.\run_server.ps1
```

**Windows Command Prompt:**
```cmd
build.bat
```

**Linux/Mac:**
```bash
./build.sh
```

## 📁 Project Structure

```
ecommerce/
├── ecommerce/           # Main project settings
│   ├── settings.py      # Configuration
│   ├── urls.py         # Main URL routing
│   └── wsgi.py         # WSGI application
├── products/           # Products app
│   ├── models.py       # Database models
│   ├── views.py        # View functions
│   ├── urls.py         # App URL routing
│   ├── admin.py        # Admin configuration
│   ├── forms.py        # Forms
│   └── templates/      # HTML templates
├── media/              # Uploaded images
├── templates/          # Global templates
├── env/               # Virtual environment
├── db.sqlite3         # SQLite database
└── requirements.txt   # Dependencies
```

## 🎨 Design Features

### Header
- **Sky blue color scheme** as requested
- **Properly aligned elements**: Logo, delivery location, search bar, account menu, returns & orders, and cart
- **Fixed header** that stays at the top while scrolling
- **Responsive design** that works on mobile devices

### Homepage
- **Dynamic banner carousel** with smooth transitions
- **Featured products section** with product cards
- **Categories section** for easy navigation
- **Professional layout** with proper spacing and typography

### Product Pages
- **Product listing** with grid layout
- **Product detail pages** with images and descriptions
- **Category filtering** (ready for enhancement)

## 🔧 Administration

Access the admin panel at `/admin/` with your superuser credentials to:

- **Manage Products**: Add, edit, delete products with images
- **Manage Categories**: Organize products into categories
- **Manage Banners**: Create promotional banners for homepage
- **View Reviews**: Monitor customer reviews
- **User Management**: Handle user accounts and permissions

## 📊 Sample Data

The project includes sample data for testing:
- 4 product categories (Electronics, Clothing, Home & Garden, Sports)
- 6 sample products with realistic pricing
- 3 promotional banners

## 🚀 Production Deployment

### Docker Deployment

The project includes Docker configuration:

```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Environment Variables

For production, set these environment variables:
- `DEBUG=False`
- `SECRET_KEY=your-secret-key`
- `DATABASE_URL=your-database-url`

## 🎯 Complete User Workflow

### Customer Journey:
1. **Browse Products**: Visit homepage → Click "Shop" → Browse product catalog
2. **Product Details**: Click any product → View details → Select quantity
3. **Add to Cart**: Click "Add to Cart" → See cart counter update
4. **Manage Cart**: Click cart icon → Update quantities → Remove items
5. **User Account**: Click "Sign Up" → Register → Login to your account
6. **Checkout**: Click "Proceed to Checkout" → Fill billing info → Enter payment
7. **Complete Order**: Use test card → Complete payment → View order confirmation
8. **Order History**: Visit profile → View "Order History" → Track all orders

### Admin Management:
1. **Access Admin**: http://127.0.0.1:8000/admin/ → Login with superuser
2. **Add Products**: Products → Add Product → Upload images and set details
3. **Manage Orders**: Orders → View order details → Update order status
4. **User Management**: Users → View registered customers

## 💳 Stripe Payment Testing

### Test Card Numbers:
- **Successful Payment**: `4242 4242 4242 4242`
- **Declined Payment**: `4000 0000 0000 0002`
- **Insufficient Funds**: `4000 0000 0000 9995`
- **Expiry**: Any future date (e.g., 12/25)
- **CVC**: Any 3 digits (e.g., 123)

### Payment Integration Setup:
1. **Get Stripe Keys**: Sign up at [stripe.com](https://stripe.com) → Get API keys
2. **Update Settings**: Edit `ecommerce/settings.py`:
   ```python
   STRIPE_PUBLISHABLE_KEY = 'pk_test_your_key_here'
   STRIPE_SECRET_KEY = 'sk_test_your_key_here'
   ```
3. **Test Payments**: Use test card numbers above during checkout

## 🔜 Next Steps & Enhancements

### Ready to Implement:
1. **User Authentication**
   - Registration and login pages
   - User profiles
   - Password reset functionality

2. **Shopping Cart**
   - Add to cart functionality
   - Cart management
   - Checkout process

3. **Payment Integration**
   - Stripe or PayPal integration
   - Order management
   - Payment confirmations

4. **Search & Filtering**
   - Product search functionality
   - Advanced filtering by price, category
   - Sorting options

5. **Reviews & Ratings**
   - Customer review system
   - Rating display
   - Review management

### UI Improvements:
1. **Enhanced Mobile Experience**
2. **Product Image Zoom**
3. **Wishlist Functionality**
4. **Recently Viewed Products**
5. **Product Recommendations**

## 🐛 Troubleshooting

### Common Issues:

1. **Server won't start**
   - Ensure virtual environment is activated
   - Check if port 8000 is available
   - Run migrations if needed

2. **Images not displaying**
   - Images show placeholder icons until uploaded via admin
   - Check MEDIA_URL and MEDIA_ROOT settings
   - Ensure images are uploaded properly
   - Verify file permissions

3. **Database errors**
   - Run `python manage.py migrate`
   - Check database connection settings

4. **"The 'image' attribute has no file associated with it" error**
   - This was fixed by adding proper image handling in templates
   - Products and banners without images now show placeholders
   - Upload images via admin panel to replace placeholders

### Image Upload Guide:

To add professional-looking images to your e-commerce site:

1. **Access Admin Panel**: http://127.0.0.1:8000/admin/
2. **Add Product Images**: Go to Products → Edit any product → Upload image
3. **Add Banner Images**: Go to Banners → Edit any banner → Upload image
4. **Use Banner Upload Form**: http://127.0.0.1:8000/products/upload-banner/

**Recommended Image Sizes:**
- Product images: 400x400 pixels (square)
- Banner images: 1920x1080 pixels (16:9 ratio)

### Check Image Status:
```bash
python manage.py add_sample_images
```

## 📝 Development Notes

- The project uses SQLite for development and PostgreSQL for production
- Bootstrap 5 is loaded via CDN for faster development
- Images are stored in the `media/` directory
- Static files are configured for production deployment

## 🤝 Contributing

To contribute to this project:
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---

**Happy coding! 🎉**

For questions or support, please refer to the Django documentation or create an issue in the project repository.
