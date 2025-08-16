# Riya Group E-commerce Production Deployment Script (PowerShell)
# This script sets up the application for production deployment on Windows

Write-Host "🚀 Starting Riya Group E-commerce Production Setup..." -ForegroundColor Green

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install production requirements
Write-Host "📦 Installing production requirements..." -ForegroundColor Cyan
pip install -r requirements.txt

# Set environment to production
$env:DJANGO_SETTINGS_MODULE = "ecommerce.settings.production"

# Create logs directory
if (!(Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs"
}

# Collect static files
Write-Host "📁 Collecting static files..." -ForegroundColor Cyan
python manage.py collectstatic --noinput

# Compress static files
Write-Host "🗜️ Compressing static files..." -ForegroundColor Cyan
python manage.py compress --force

# Run database migrations
Write-Host "🗄️ Running database migrations..." -ForegroundColor Cyan
python manage.py migrate

# Create superuser (if needed)
Write-Host "👤 Creating superuser (if not exists)..." -ForegroundColor Cyan
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
Write-Host "📊 Loading sample data..." -ForegroundColor Cyan
try {
    python manage.py populate_data
} catch {
    Write-Host "Sample data already exists" -ForegroundColor Yellow
}

# Run security check
Write-Host "🔒 Running security checks..." -ForegroundColor Cyan
python manage.py check --deploy

Write-Host "✅ Production setup completed!" -ForegroundColor Green
Write-Host "Your Riya Group e-commerce site is ready for deployment!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Set up your environment variables (.env file)"
Write-Host "2. Configure your web server (IIS/Nginx)"
Write-Host "3. Set up your database (PostgreSQL)"
Write-Host "4. Configure Redis for caching"
Write-Host "5. Set up SSL certificates"
Write-Host ""
Write-Host "To start the production server:" -ForegroundColor Cyan
Write-Host "gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000"
