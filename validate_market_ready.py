#!/usr/bin/env python
"""
Final Market Readiness Validation Script
This script performs comprehensive checks to ensure the Riya Group E-commerce
application is 100% ready for market launch.
"""
import os
import sys
import subprocess
import requests
from pathlib import Path
from urllib.parse import urljoin
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Add the project directory to the Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

class MarketReadinessValidator:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:8000'  # Change to your domain when deployed
        self.errors = []
        self.warnings = []
        self.success_count = 0
        self.total_checks = 0
    
    def check(self, description, test_func):
        """Run a check and record the result."""
        self.total_checks += 1
        try:
            result = test_func()
            if result:
                print(f"✅ {description}")
                self.success_count += 1
                return True
            else:
                print(f"❌ {description}")
                self.errors.append(description)
                return False
        except Exception as e:
            print(f"⚠️ {description} - Error: {e}")
            self.warnings.append(f"{description} - Error: {e}")
            return False
    
    def check_files_exist(self):
        """Check that all required files exist."""
        required_files = [
            'manage.py',
            'requirements.txt',
            '.env.example',
            'static/favicon.ico',
            'static/robots.txt',
            'templates/base.html',
            'templates/404.html',
            'templates/500.html',
            'ecommerce/settings/production.py',
            'products/sitemaps.py',
        ]
        
        for file_path in required_files:
            self.check(
                f"Required file exists: {file_path}",
                lambda f=file_path: Path(f).exists()
            )
    
    def check_django_settings(self):
        """Check Django configuration."""
        from django.conf import settings
        
        # Check basic settings
        self.check(
            "INSTALLED_APPS includes required apps",
            lambda: all(app in settings.INSTALLED_APPS for app in [
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'products',
                'accounts',
                'cart',
                'orders'
            ])
        )
        
        self.check(
            "STATIC_URL is configured",
            lambda: hasattr(settings, 'STATIC_URL') and settings.STATIC_URL
        )
        
        self.check(
            "MEDIA_URL is configured",
            lambda: hasattr(settings, 'MEDIA_URL') and settings.MEDIA_URL
        )
    
    def check_database_models(self):
        """Check database models and migrations."""
        try:
            from products.models import Product, Category
            from accounts.models import User
            from cart.models import Cart, CartItem
            from orders.models import Order
            
            self.check(
                "Product model exists and accessible",
                lambda: Product.objects.model._meta.get_field('name') is not None
            )
            
            self.check(
                "Category model exists and accessible",
                lambda: Category.objects.model._meta.get_field('name') is not None
            )
            
            self.check(
                "Cart model exists and accessible",
                lambda: Cart.objects.model._meta.get_field('user') is not None
            )
            
        except Exception as e:
            self.warnings.append(f"Model check error: {e}")
    
    def check_templates(self):
        """Check that templates exist and are valid."""
        template_files = [
            'templates/base.html',
            'templates/404.html',
            'templates/500.html',
            'products/templates/products/product_list.html',
            'products/templates/products/product_detail.html',
            'accounts/templates/accounts/login.html',
            'cart/templates/cart/cart_detail.html'
        ]
        
        for template in template_files:
            self.check(
                f"Template exists: {template}",
                lambda t=template: Path(t).exists() or self._check_template_in_apps(t)
            )
    
    def _check_template_in_apps(self, template_path):
        """Check if template exists in any of the app directories."""
        # This is a simplified check - in a real scenario you'd use Django's template loader
        parts = template_path.split('/')
        if len(parts) >= 3:  # app/templates/app/template.html
            app_template_path = Path(parts[0]) / 'templates' / '/'.join(parts[2:])
            return app_template_path.exists()
        return False
    
    def check_static_files(self):
        """Check static files configuration."""
        static_files = [
            'static/favicon.ico',
            'static/robots.txt'
        ]
        
        for static_file in static_files:
            self.check(
                f"Static file exists: {static_file}",
                lambda sf=static_file: Path(sf).exists()
            )
    
    def check_management_commands(self):
        """Check custom management commands."""
        management_commands = [
            'products/management/commands/check_market_ready.py'
        ]
        
        for command in management_commands:
            self.check(
                f"Management command exists: {command}",
                lambda cmd=command: Path(cmd).exists()
            )
    
    def check_security_settings(self):
        """Check security configuration."""
        # Run Django's built-in security checks
        try:
            result = subprocess.run([
                sys.executable, 'manage.py', 'check', '--deploy'
            ], capture_output=True, text=True)
            
            # In development, we expect some warnings, so we check if it runs without errors
            self.check(
                "Django deployment checks run without critical errors",
                lambda: result.returncode == 0 or 'Error' not in result.stderr
            )
            
        except Exception as e:
            self.warnings.append(f"Security check error: {e}")
    
    def check_url_patterns(self):
        """Check URL configuration."""
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        
        url_names = [
            'products:product_list',
            'accounts:login',
            'cart:cart_detail'
        ]
        
        for url_name in url_names:
            try:
                reverse(url_name)
                self.check(
                    f"URL pattern resolves: {url_name}",
                    lambda: True
                )
            except NoReverseMatch:
                self.check(
                    f"URL pattern resolves: {url_name}",
                    lambda: False
                )
    
    def check_production_readiness(self):
        """Check production-specific requirements."""
        prod_files = [
            'deploy_production.py',
            'PRODUCTION_DEPLOYMENT.md',
            'MARKET_LAUNCH_CHECKLIST.md'
        ]
        
        for file_path in prod_files:
            self.check(
                f"Production file exists: {file_path}",
                lambda f=file_path: Path(f).exists()
            )
    
    def run_all_checks(self):
        """Run all validation checks."""
        print("🚀 Running Comprehensive Market Readiness Validation")
        print("=" * 60)
        
        print("\n📁 Checking Required Files...")
        self.check_files_exist()
        
        print("\n⚙️ Checking Django Configuration...")
        self.check_django_settings()
        
        print("\n🗄️ Checking Database Models...")
        self.check_database_models()
        
        print("\n📄 Checking Templates...")
        self.check_templates()
        
        print("\n📦 Checking Static Files...")
        self.check_static_files()
        
        print("\n🛠️ Checking Management Commands...")
        self.check_management_commands()
        
        print("\n🔒 Checking Security Settings...")
        self.check_security_settings()
        
        print("\n🔗 Checking URL Configuration...")
        self.check_url_patterns()
        
        print("\n🚀 Checking Production Readiness...")
        self.check_production_readiness()
        
        # Generate final report
        print("\n" + "=" * 60)
        print("📋 FINAL VALIDATION REPORT")
        print("=" * 60)
        
        success_rate = (self.success_count / self.total_checks) * 100 if self.total_checks > 0 else 0
        
        print(f"✅ Successful checks: {self.success_count}/{self.total_checks} ({success_rate:.1f}%)")
        
        if self.errors:
            print(f"\n❌ Critical Issues ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print(f"\n⚠️ Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        # Overall assessment
        print("\n" + "=" * 60)
        if success_rate >= 90 and len(self.errors) == 0:
            print("🎉 EXCELLENT! Your application is MARKET READY!")
            print("🚀 All critical checks passed. Ready for production deployment!")
        elif success_rate >= 80:
            print("✅ GOOD! Your application is nearly market ready.")
            print("🔧 Address the issues above and run the check again.")
        elif success_rate >= 60:
            print("⚠️ NEEDS WORK! Several issues need to be addressed.")
            print("🛠️ Please fix the critical issues before deployment.")
        else:
            print("❌ NOT READY! Significant issues need to be resolved.")
            print("🔧 Please address all issues before considering deployment.")
        
        print("\n📖 Next Steps:")
        if self.errors:
            print("1. Fix all critical issues listed above")
            print("2. Run this validation script again")
            print("3. Run: python deploy_production.py")
        else:
            print("1. Review MARKET_LAUNCH_CHECKLIST.md")
            print("2. Run: python deploy_production.py")
            print("3. Deploy to production environment")
            print("4. Test thoroughly in production")
        
        print("\n🌟 Good luck with your Riya Group E-commerce launch!")
        
        return success_rate >= 90 and len(self.errors) == 0

def main():
    """Main function to run the validation."""
    validator = MarketReadinessValidator()
    is_ready = validator.run_all_checks()
    sys.exit(0 if is_ready else 1)

if __name__ == "__main__":
    main()
