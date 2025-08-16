@echo off
REM Build script for Django ecommerce project (Windows)

echo 🚀 Building Django E-commerce Project...

REM Activate virtual environment
echo 📦 Activating virtual environment...
call env\Scripts\activate.bat

REM Install requirements
echo 📋 Installing requirements...
pip install -r requirements.txt

REM Run migrations
echo 🔄 Running migrations...
python manage.py makemigrations
python manage.py migrate

REM Load sample data
echo 📊 Loading sample data...
python manage.py load_sample_data

REM Collect static files (for production)
echo 📁 Collecting static files...
python manage.py collectstatic --noinput

echo ✅ Build complete!
echo 🌐 You can now run: python manage.py runserver
echo 🔗 Visit: http://127.0.0.1:8000

pause
