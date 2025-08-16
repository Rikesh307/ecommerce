#!/usr/bin/env python
"""
Production Deployment Script for Riya Group E-commerce
This script helps deploy the application to production with all security checks.
"""
import os
import sys
import subprocess
import secrets
import string
from pathlib import Path

def generate_secret_key():
    """Generate a secure Django secret key."""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for i in range(50))

def create_production_env():
    """Create a production .env file template."""
    secret_key = generate_secret_key()
    
    env_content = f"""# Production Environment Variables for Riya Group E-commerce
# SECURITY WARNING: Keep these values secret and secure!

# Django Settings
SECRET_KEY={secret_key}
DEBUG=False
DJANGO_SETTINGS_MODULE=ecommerce.settings.production

# Allowed Hosts (comma-separated)
ALLOWED_HOST=riyagroup.com

# Database Configuration (PostgreSQL recommended for production)
DB_NAME=riyagroup_ecommerce
DB_USER=riyagroup_user
DB_PASSWORD=YOUR_SECURE_DATABASE_PASSWORD
DB_HOST=localhost
DB_PORT=5432

# Redis Cache Configuration
REDIS_URL=redis://127.0.0.1:6379/1

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@riyagroup.com
EMAIL_HOST_PASSWORD=YOUR_EMAIL_PASSWORD

# AWS S3 Configuration (optional for media files)
USE_S3=FALSE
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

# Monitoring and Error Tracking
SENTRY_DSN=

# SSL and Security (automatically set to True in production settings)
# These are handled by the production settings file
"""
    
    with open('.env.production', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env.production template")
    print("🔧 Please update the values in .env.production before deployment")

def run_security_checks():
    """Run Django security checks."""
    print("\n🔒 Running Django security checks...")
    result = subprocess.run([
        sys.executable, 'manage.py', 'check', '--deploy', '--settings=ecommerce.settings.production'
    ], capture_output=True, text=True, env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'ecommerce.settings.production'})
    
    if result.returncode != 0:
        print("❌ Security checks failed:")
        print(result.stderr)
        return False
    else:
        print("✅ Security checks passed")
        return True

def collect_static_files():
    """Collect static files for production."""
    print("\n📦 Collecting static files...")
    result = subprocess.run([
        sys.executable, 'manage.py', 'collectstatic', '--noinput', '--settings=ecommerce.settings.production'
    ], capture_output=True, text=True, env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'ecommerce.settings.production'})
    
    if result.returncode != 0:
        print("❌ Static file collection failed:")
        print(result.stderr)
        return False
    else:
        print("✅ Static files collected successfully")
        return True

def compress_static_files():
    """Compress static files for production."""
    print("\n🗜️ Compressing static files...")
    result = subprocess.run([
        sys.executable, 'manage.py', 'compress', '--settings=ecommerce.settings.production'
    ], capture_output=True, text=True, env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'ecommerce.settings.production'})
    
    if result.returncode != 0:
        print("⚠️ Static file compression failed (this is optional):")
        print(result.stderr)
        return False
    else:
        print("✅ Static files compressed successfully")
        return True

def run_migrations():
    """Run database migrations."""
    print("\n🗄️ Running database migrations...")
    result = subprocess.run([
        sys.executable, 'manage.py', 'migrate', '--settings=ecommerce.settings.production'
    ], capture_output=True, text=True, env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'ecommerce.settings.production'})
    
    if result.returncode != 0:
        print("❌ Database migrations failed:")
        print(result.stderr)
        return False
    else:
        print("✅ Database migrations completed")
        return True

def create_superuser():
    """Create a superuser account."""
    print("\n👤 Creating superuser account...")
    print("You will need to create an admin user for the production site.")
    result = subprocess.run([
        sys.executable, 'manage.py', 'createsuperuser', '--settings=ecommerce.settings.production'
    ], env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'ecommerce.settings.production'})
    
    return result.returncode == 0

def run_final_checks():
    """Run final market readiness checks."""
    print("\n🏁 Running final market readiness checks...")
    result = subprocess.run([
        sys.executable, 'manage.py', 'check_market_ready'
    ], env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'ecommerce.settings.production'})
    
    return result.returncode == 0

def main():
    """Main deployment function."""
    print("🚀 Riya Group E-commerce Production Deployment")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Create production environment file
    create_production_env()
    
    # Load production environment (if .env.production exists)
    if Path('.env.production').exists():
        print("\n📋 Please ensure all values in .env.production are correctly set before continuing.")
        input("Press Enter to continue when ready...")
    
    steps = [
        ("Security Checks", run_security_checks),
        ("Static Files Collection", collect_static_files),
        ("Static Files Compression", compress_static_files),
        ("Database Migrations", run_migrations),
        ("Final Market Readiness Check", run_final_checks),
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        try:
            if not step_func():
                failed_steps.append(step_name)
        except Exception as e:
            print(f"❌ {step_name} failed with error: {e}")
            failed_steps.append(step_name)
    
    # Optionally create superuser
    print("\n" + "=" * 50)
    create_superuser_choice = input("Do you want to create a superuser account? (y/N): ").lower().strip()
    if create_superuser_choice in ['y', 'yes']:
        create_superuser()
    
    # Final summary
    print("\n" + "=" * 50)
    print("🎯 DEPLOYMENT SUMMARY")
    print("=" * 50)
    
    if failed_steps:
        print("❌ Some steps failed:")
        for step in failed_steps:
            print(f"  - {step}")
        print("\n🔧 Please fix the issues above before deploying to production.")
    else:
        print("✅ All deployment checks passed!")
        print("\n🌟 Your Riya Group E-commerce application is ready for production!")
        print("\n📋 Next steps:")
        print("1. Review and update .env.production with your actual values")
        print("2. Set up your production database (PostgreSQL recommended)")
        print("3. Set up Redis for caching")
        print("4. Configure your web server (nginx + gunicorn recommended)")
        print("5. Set up SSL certificate")
        print("6. Configure your domain DNS")
        print("7. Set up monitoring and backups")
        print("8. Test the live site thoroughly")
    
    print("\n🚀 Happy launching!")

if __name__ == "__main__":
    main()
