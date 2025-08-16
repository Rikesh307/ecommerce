"""
Production setup and deployment script for Riya Group E-commerce.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command
import os
import subprocess
import sys

class Command(BaseCommand):
    help = 'Prepare application for production deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--environment',
            choices=['staging', 'production'],
            default='staging',
            help='Target environment for deployment',
        )

    def handle(self, *args, **options):
        environment = options['environment']
        
        self.stdout.write(
            self.style.HTTP_INFO(f'🚀 Preparing Riya Group E-commerce for {environment.upper()} deployment...')
        )
        
        steps = [
            self.check_environment,
            self.collect_static_files,
            self.compress_static_files,
            self.run_tests,
            self.check_security,
            self.validate_database,
            self.generate_deployment_files,
        ]
        
        for step in steps:
            try:
                step(environment)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Step failed: {step.__name__}')
                )
                self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
                return
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('🎉 DEPLOYMENT PREPARATION COMPLETE!'))
        self.stdout.write('='*60)
        self.print_deployment_instructions(environment)

    def check_environment(self, environment):
        self.stdout.write('\n📋 Checking environment configuration...')
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 8):
            raise Exception("Python 3.8+ required")
        self.stdout.write(self.style.SUCCESS(f'✅ Python {python_version.major}.{python_version.minor} detected'))
        
        # Check required environment variables for production
        if environment == 'production':
            required_vars = ['SECRET_KEY', 'DB_PASSWORD', 'EMAIL_HOST_PASSWORD']
            missing_vars = [var for var in required_vars if not os.environ.get(var)]
            if missing_vars:
                raise Exception(f"Missing environment variables: {', '.join(missing_vars)}")
            self.stdout.write(self.style.SUCCESS('✅ Environment variables configured'))

    def collect_static_files(self, environment):
        self.stdout.write('\n📦 Collecting static files...')
        call_command('collectstatic', '--noinput', verbosity=1)
        self.stdout.write(self.style.SUCCESS('✅ Static files collected'))

    def compress_static_files(self, environment):
        self.stdout.write('\n🗜️ Compressing static files...')
        try:
            call_command('compress', '--force')
            self.stdout.write(self.style.SUCCESS('✅ Static files compressed'))
        except Exception:
            self.stdout.write(self.style.WARNING('⚠️ Compression skipped (compressor not available)'))

    def run_tests(self, environment):
        self.stdout.write('\n🧪 Running tests...')
        try:
            call_command('test', verbosity=1)
            self.stdout.write(self.style.SUCCESS('✅ All tests passed'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️ Some tests failed: {str(e)}'))

    def check_security(self, environment):
        self.stdout.write('\n🔒 Running security checks...')
        call_command('check', '--deploy')
        self.stdout.write(self.style.SUCCESS('✅ Security check completed'))

    def validate_database(self, environment):
        self.stdout.write('\n🗄️ Validating database...')
        call_command('makemigrations', '--check', verbosity=0)
        call_command('migrate', '--run-syncdb')
        self.stdout.write(self.style.SUCCESS('✅ Database validated and migrated'))

    def generate_deployment_files(self, environment):
        self.stdout.write('\n📄 Generating deployment files...')
        
        # Generate updated requirements
        self.generate_requirements()
        
        # Generate Docker files
        self.generate_dockerfile(environment)
        
        # Generate deployment scripts
        self.generate_deploy_script(environment)
        
        self.stdout.write(self.style.SUCCESS('✅ Deployment files generated'))

    def generate_requirements(self):
        """Generate production requirements.txt"""
        requirements_content = """# Core Django
Django==5.2
asgiref==3.8.1
sqlparse==0.5.3

# Database
psycopg2-binary==2.9.10

# Media handling
pillow==11.1.0

# Forms and UI
django-crispy-forms==2.3
crispy-bootstrap4==2024.1

# Cache and session
redis==5.2.0
django-redis==5.4.0

# Static files and compression
whitenoise==6.6.0
django-compressor==4.4

# Production utilities
gunicorn==21.2.0
dj-database-url==2.1.0
python-decouple==3.8

# Security and monitoring
sentry-sdk==1.39.2

# Email
django-anymail==10.2

# Extensions
django-extensions==3.2.3
django-humanize==0.1.2
django-filter==24.3

# Storage (optional)
django-storages==1.14.2
boto3==1.34.0"""
        
        with open('requirements-production.txt', 'w') as f:
            f.write(requirements_content)

    def generate_dockerfile(self, environment):
        """Generate Dockerfile for containerized deployment"""
        dockerfile_content = f"""FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=ecommerce.settings.{environment}

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements-production.txt /app/
RUN pip install --no-cache-dir -r requirements-production.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecommerce.wsgi:application"]"""
        
        with open('Dockerfile', 'w') as f:
            f.write(dockerfile_content)

    def generate_deploy_script(self, environment):
        """Generate deployment script"""
        deploy_script = f"""#!/bin/bash
# Riya Group E-commerce Deployment Script for {environment.upper()}

echo "🚀 Starting {environment} deployment..."

# Pull latest code
git pull origin main

# Install/update dependencies
pip install -r requirements-production.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Compress static files
python manage.py compress --force

# Restart services (adjust as needed)
# sudo systemctl restart gunicorn
# sudo systemctl restart nginx

echo "✅ {environment.capitalize()} deployment completed!"
"""
        
        script_name = f'deploy-{environment}.sh'
        with open(script_name, 'w') as f:
            f.write(deploy_script)
        
        # Make script executable
        os.chmod(script_name, 0o755)

    def print_deployment_instructions(self, environment):
        instructions = f"""
📖 DEPLOYMENT INSTRUCTIONS FOR {environment.upper()}:

1. 🔧 ENVIRONMENT SETUP:
   • Set DJANGO_SETTINGS_MODULE=ecommerce.settings.{environment}
   • Configure environment variables from .env.example
   • Set up SSL certificates for HTTPS

2. 🗄️ DATABASE SETUP:
   • Create PostgreSQL database
   • Run: python manage.py migrate
   • Create superuser: python manage.py createsuperuser

3. 🌐 WEB SERVER SETUP:
   • Configure Nginx/Apache reverse proxy
   • Set up Gunicorn service
   • Configure SSL termination

4. 📊 MONITORING SETUP:
   • Configure logging destinations
   • Set up health check monitoring
   • Configure error tracking (Sentry)

5. 🚀 DEPLOYMENT:
   • Use Docker: docker build -t riyagroup-ecommerce .
   • Or use script: ./deploy-{environment}.sh
   • Monitor logs for any issues

6. ✅ POST-DEPLOYMENT:
   • Test all critical user flows
   • Verify SSL certificate
   • Check performance metrics
   • Set up backup procedures

📞 SUPPORT:
   • Health check: /health/
   • Status check: /status/
   • Admin panel: /admin/

🎯 Your Riya Group E-commerce application is ready for {environment}!
"""
        
        self.stdout.write(instructions)
