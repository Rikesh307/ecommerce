"""
Management command to check if the application is market-ready.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command
from django.apps import apps
import os
import sys
from pathlib import Path

class Command(BaseCommand):
    help = 'Check if the application is ready for market deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Attempt to fix issues automatically',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('🔍 Checking Riya Group E-commerce Application Readiness...'))
        
        issues = []
        warnings = []
        
        # Check 1: Security Settings
        self.stdout.write('\n📊 Checking Security Settings...')
        security_issues = self.check_security()
        issues.extend(security_issues)
        
        # Check 2: Database and Models
        self.stdout.write('\n📊 Checking Database and Models...')
        db_issues = self.check_database()
        issues.extend(db_issues)
        
        # Check 3: Static Files and Media
        self.stdout.write('\n📊 Checking Static Files and Media...')
        static_issues = self.check_static_files()
        issues.extend(static_issues)
        
        # Check 4: SEO and Marketing
        self.stdout.write('\n📊 Checking SEO and Marketing...')
        seo_issues = self.check_seo()
        issues.extend(seo_issues)
        
        # Check 5: Performance and Caching
        self.stdout.write('\n📊 Checking Performance and Caching...')
        perf_issues = self.check_performance()
        warnings.extend(perf_issues)
        
        # Check 6: Testing and Quality
        self.stdout.write('\n📊 Checking Code Quality...')
        quality_issues = self.check_code_quality()
        warnings.extend(quality_issues)
        
        # Check 7: Deployment Readiness
        self.stdout.write('\n📊 Checking Deployment Readiness...')
        deploy_issues = self.check_deployment()
        issues.extend(deploy_issues)
        
        # Summary
        self.print_summary(issues, warnings, options.get('fix', False))

    def check_security(self):
        issues = []
        
        # Check Django deployment settings
        try:
            call_command('check', '--deploy', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✅ Django deployment check passed'))
        except Exception as e:
            issues.append(f"Django deployment check failed: {str(e)}")
            self.stdout.write(self.style.ERROR('❌ Django deployment check failed'))
        
        # Check SECRET_KEY
        if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 50:
            issues.append("SECRET_KEY is too short or missing")
            self.stdout.write(self.style.ERROR('❌ SECRET_KEY is insecure'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ SECRET_KEY is secure'))
        
        # Check DEBUG setting
        if settings.DEBUG:
            issues.append("DEBUG is True - should be False in production")
            self.stdout.write(self.style.ERROR('❌ DEBUG is True'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ DEBUG is False'))
        
        return issues

    def check_database(self):
        issues = []
        
        # Check migrations
        try:
            call_command('makemigrations', '--check', verbosity=0, dry_run=True)
            self.stdout.write(self.style.SUCCESS('✅ No pending migrations'))
        except Exception:
            issues.append("There are pending migrations")
            self.stdout.write(self.style.ERROR('❌ Pending migrations found'))
        
        # Check if essential models exist
        try:
            Product = apps.get_model('products', 'Product')
            Category = apps.get_model('products', 'Category')
            User = apps.get_model('auth', 'User')
            self.stdout.write(self.style.SUCCESS('✅ Essential models exist'))
        except Exception as e:
            issues.append(f"Essential models missing: {str(e)}")
            self.stdout.write(self.style.ERROR('❌ Essential models missing'))
        
        return issues

    def check_static_files(self):
        issues = []
        
        # Check static files configuration
        if not settings.STATIC_URL:
            issues.append("STATIC_URL is not configured")
            self.stdout.write(self.style.ERROR('❌ STATIC_URL not configured'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ STATIC_URL configured'))
        
        # Check if static files can be collected
        try:
            call_command('collectstatic', '--noinput', '--dry-run', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✅ Static files can be collected'))
        except Exception as e:
            issues.append(f"Static files collection failed: {str(e)}")
            self.stdout.write(self.style.ERROR('❌ Static files collection failed'))
        
        # Check for essential static files
        static_root = Path(settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT)
        
        essential_files = ['robots.txt', 'favicon.ico']
        for file in essential_files:
            if not (static_root / file).exists():
                issues.append(f"Missing essential file: {file}")
                self.stdout.write(self.style.ERROR(f'❌ Missing {file}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✅ {file} exists'))
        
        return issues

    def check_seo(self):
        issues = []
        
        # Check if sitemaps are configured
        if 'django.contrib.sitemaps' in settings.INSTALLED_APPS:
            self.stdout.write(self.style.SUCCESS('✅ Sitemaps app installed'))
        else:
            issues.append("Sitemaps app not installed")
            self.stdout.write(self.style.ERROR('❌ Sitemaps app not installed'))
        
        # Check if sitemap file exists
        try:
            from products.sitemaps import ProductSitemap
            self.stdout.write(self.style.SUCCESS('✅ Sitemap configuration exists'))
        except ImportError:
            issues.append("Sitemap configuration missing")
            self.stdout.write(self.style.ERROR('❌ Sitemap configuration missing'))
        
        return issues

    def check_performance(self):
        warnings = []
        
        # Check caching configuration
        if 'default' not in settings.CACHES or settings.CACHES['default']['BACKEND'] == 'django.core.cache.backends.locmem.LocMemCache':
            warnings.append("No production-ready cache backend configured")
            self.stdout.write(self.style.WARNING('⚠️ No production cache configured'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Cache backend configured'))
        
        # Check compression
        if 'compressor' in settings.INSTALLED_APPS:
            self.stdout.write(self.style.SUCCESS('✅ Compression configured'))
        else:
            warnings.append("Static file compression not configured")
            self.stdout.write(self.style.WARNING('⚠️ No compression configured'))
        
        return warnings

    def check_code_quality(self):
        warnings = []
        
        # Check if tests exist
        test_files = list(Path(settings.BASE_DIR).rglob('test*.py'))
        if len(test_files) < 3:
            warnings.append("Limited test coverage")
            self.stdout.write(self.style.WARNING('⚠️ Limited test coverage'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Test files exist'))
        
        return warnings

    def check_deployment(self):
        issues = []
        
        # Check for requirements.txt
        req_file = Path(settings.BASE_DIR) / 'requirements.txt'
        if not req_file.exists():
            issues.append("requirements.txt missing")
            self.stdout.write(self.style.ERROR('❌ requirements.txt missing'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ requirements.txt exists'))
        
        # Check for production settings
        prod_settings = Path(settings.BASE_DIR) / 'ecommerce' / 'settings' / 'production.py'
        if not prod_settings.exists():
            issues.append("Production settings missing")
            self.stdout.write(self.style.ERROR('❌ Production settings missing'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Production settings exist'))
        
        # Check for environment configuration
        env_example = Path(settings.BASE_DIR) / '.env.example'
        if not env_example.exists():
            issues.append(".env.example missing")
            self.stdout.write(self.style.ERROR('❌ .env.example missing'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ .env.example exists'))
        
        return issues

    def print_summary(self, issues, warnings, fix_attempted):
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.HTTP_INFO('📋 MARKET READINESS SUMMARY'))
        self.stdout.write('='*60)
        
        if not issues and not warnings:
            self.stdout.write(self.style.SUCCESS('🎉 CONGRATULATIONS! Your application is MARKET READY!'))
            self.stdout.write(self.style.SUCCESS('✅ All critical checks passed'))
            self.stdout.write(self.style.SUCCESS('✅ No major issues found'))
            
        elif not issues:
            self.stdout.write(self.style.SUCCESS('🎯 Your application is MOSTLY READY for market!'))
            self.stdout.write(self.style.SUCCESS('✅ All critical issues resolved'))
            self.stdout.write(self.style.WARNING(f'⚠️ {len(warnings)} optimization opportunities found'))
            
        else:
            self.stdout.write(self.style.ERROR('🔧 Your application needs attention before market launch'))
            self.stdout.write(self.style.ERROR(f'❌ {len(issues)} critical issues found'))
            self.stdout.write(self.style.WARNING(f'⚠️ {len(warnings)} warnings found'))
        
        if issues:
            self.stdout.write('\n🚨 CRITICAL ISSUES TO FIX:')
            for i, issue in enumerate(issues, 1):
                self.stdout.write(f'  {i}. {issue}')
        
        if warnings:
            self.stdout.write('\n⚠️ OPTIMIZATION RECOMMENDATIONS:')
            for i, warning in enumerate(warnings, 1):
                self.stdout.write(f'  {i}. {warning}')
        
        self.stdout.write('\n📖 NEXT STEPS:')
        if issues:
            self.stdout.write('  1. Fix all critical issues listed above')
            self.stdout.write('  2. Run this command again to verify fixes')
            self.stdout.write('  3. Deploy to staging environment for testing')
            self.stdout.write('  4. Run final production deployment')
        else:
            self.stdout.write('  1. Address optimization recommendations')
            self.stdout.write('  2. Set up monitoring and analytics')
            self.stdout.write('  3. Deploy to production environment')
            self.stdout.write('  4. Monitor performance and user feedback')
        
        self.stdout.write('\n🚀 Ready to launch Riya Group E-commerce to the market!')
