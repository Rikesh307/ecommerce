#!/usr/bin/env bash

# Riya Group E-commerce Production Deployment Script
# This script sets up the application for production deployment

set -e

echo "🚀 Starting Riya Group E-commerce Production Setup..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install production requirements
echo "📦 Installing production requirements..."
pip install -r requirements.txt

# Set environment to production
export DJANGO_SETTINGS_MODULE=ecommerce.settings.production

# Create logs directory
mkdir -p logs

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Compress static files
echo "🗜️ Compressing static files..."
python manage.py compress --force

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser (if needed)
echo "👤 Creating superuser (if not exists)..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@riyagroup.com', 'secure_password_123')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"

# Load sample data (optional)
echo "📊 Loading sample data..."
python manage.py populate_data || echo "Sample data already exists"

# Run security check
echo "🔒 Running security checks..."
python manage.py check --deploy

echo "✅ Production setup completed!"
echo "Your Riya Group e-commerce site is ready for deployment!"
echo ""
echo "Next steps:"
echo "1. Set up your environment variables (.env file)"
echo "2. Configure your web server (Nginx/Apache)"
echo "3. Set up your database (PostgreSQL)"
echo "4. Configure Redis for caching"
echo "5. Set up SSL certificates"
echo ""
echo "To start the production server:"
echo "gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000"
