#!/bin/bash
# Build script for Django ecommerce project

echo "🚀 Building Django E-commerce Project..."

# Activate virtual environment
echo "📦 Activating virtual environment..."
source env/bin/activate

# Install requirements
echo "📋 Installing requirements..."
pip install -r requirements.txt

# Run migrations
echo "🔄 Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Load sample data
echo "📊 Loading sample data..."
python manage.py load_sample_data

# Collect static files (for production)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build complete!"
echo "🌐 You can now run: python manage.py runserver"
echo "🔗 Visit: http://127.0.0.1:8000"
