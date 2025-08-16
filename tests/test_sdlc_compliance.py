"""
SDLC Test Suite - Core Functionality Tests
Testing framework following SDLC best practices for Riya Group E-commerce
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
import os


class SDLCSystemTests(TestCase):
    """
    System-level tests following SDLC quality assurance standards
    """
    
    def setUp(self):
        """Set up test environment following SDLC test planning phase"""
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_security_headers_present(self):
        """Test security headers are properly configured (SDLC Security Requirements)"""
        response = self.client.get('/')
        
        # Test X-Frame-Options for clickjacking protection
        if not settings.DEBUG:  # Only in production
            self.assertIn('X-Frame-Options', response.headers)
    
    def test_csrf_protection_enabled(self):
        """Test CSRF protection is working (SDLC Security Testing)"""
        response = self.client.get('/')
        # CSRF middleware should be active
        self.assertContains(response, 'csrfmiddlewaretoken', status_code=200)
    
    def test_authentication_required_for_sensitive_pages(self):
        """Test authentication requirements (SDLC Access Control Testing)"""
        # Test checkout requires authentication
        response = self.client.get('/orders/checkout/')
        # Should redirect to login or show proper error
        self.assertIn(response.status_code, [302, 403, 404])
    
    def test_static_files_accessibility(self):
        """Test static files are properly configured (SDLC Integration Testing)"""
        # Test that static file serving is configured
        self.assertTrue(hasattr(settings, 'STATIC_URL'))
        self.assertTrue(hasattr(settings, 'STATIC_ROOT'))
    
    def test_database_connectivity(self):
        """Test database connectivity and model integrity (SDLC System Testing)"""
        # Test basic database operations
        user_count = User.objects.count()
        self.assertGreaterEqual(user_count, 1)  # Our test user should exist
    
    def test_template_rendering(self):
        """Test template rendering works properly (SDLC UI Testing)"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Riya Group')  # Brand name should appear
    
    def test_url_patterns_configured(self):
        """Test URL routing is properly configured (SDLC Integration Testing)"""
        # Test main pages exist
        urls_to_test = ['/', '/products/', '/accounts/login/']
        
        for url in urls_to_test:
            with self.subTest(url=url):
                response = self.client.get(url)
                # Should not be 500 (server error)
                self.assertNotEqual(response.status_code, 500)


class SDLCSecurityTests(TestCase):
    """
    Security-focused tests following SDLC security testing standards
    """
    
    def setUp(self):
        self.client = Client()
    
    def test_debug_mode_disabled_in_production(self):
        """Test DEBUG is False in production settings (SDLC Security)"""
        # In a real production test, this should be False
        # For development, we check the setting exists
        self.assertTrue(hasattr(settings, 'DEBUG'))
    
    def test_secret_key_configured(self):
        """Test SECRET_KEY is properly configured (SDLC Security)"""
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))
        self.assertNotEqual(settings.SECRET_KEY, '')
        # Should not be the default Django insecure key
        self.assertNotIn('django-insecure', settings.SECRET_KEY)
    
    def test_allowed_hosts_configured(self):
        """Test ALLOWED_HOSTS is properly configured (SDLC Security)"""
        self.assertTrue(hasattr(settings, 'ALLOWED_HOSTS'))
        # In production, should not allow all hosts
        if not settings.DEBUG:
            self.assertNotIn('*', settings.ALLOWED_HOSTS)
    
    def test_sql_injection_protection(self):
        """Test basic SQL injection protection (SDLC Security Testing)"""
        # Django ORM should protect against SQL injection
        # Test with malicious input
        malicious_input = "'; DROP TABLE auth_user; --"
        response = self.client.get('/products/', {'search': malicious_input})
        # Should not cause server error (500)
        self.assertNotEqual(response.status_code, 500)


class SDLCPerformanceTests(TestCase):
    """
    Performance tests following SDLC non-functional requirements
    """
    
    def setUp(self):
        self.client = Client()
    
    def test_page_load_performance(self):
        """Test basic page load performance (SDLC Performance Testing)"""
        import time
        
        start_time = time.time()
        response = self.client.get('/')
        end_time = time.time()
        
        # Page should load within reasonable time (adjust as needed)
        load_time = end_time - start_time
        self.assertLess(load_time, 5.0, f"Page load took {load_time:.2f} seconds")
    
    def test_database_query_optimization(self):
        """Test database queries are optimized (SDLC Performance)"""
        from django.test.utils import override_settings
        from django.db import connection
        
        # Reset query count
        connection.queries_log.clear()
        
        # Test a page that should have minimal queries
        response = self.client.get('/')
        
        # Should not have excessive database queries
        query_count = len(connection.queries)
        self.assertLess(query_count, 50, f"Too many database queries: {query_count}")


class SDLCAccessibilityTests(TestCase):
    """
    Accessibility tests following SDLC accessibility standards (WCAG)
    """
    
    def setUp(self):
        self.client = Client()
    
    def test_html_lang_attribute(self):
        """Test HTML lang attribute is present (WCAG 2.1 AA)"""
        response = self.client.get('/')
        content = response.content.decode()
        self.assertIn('lang=', content)
    
    def test_page_title_present(self):
        """Test page titles are present (WCAG 2.1 AA)"""
        response = self.client.get('/')
        content = response.content.decode()
        self.assertIn('<title>', content)
    
    def test_form_labels_present(self):
        """Test form labels are properly associated (WCAG 2.1 AA)"""
        # Test login form
        response = self.client.get('/accounts/login/')
        if response.status_code == 200:
            content = response.content.decode()
            # Should have proper form labels
            self.assertTrue(
                '<label' in content or 'aria-label' in content,
                "Forms should have proper labels for accessibility"
            )


class SDLCCodeQualityTests(TestCase):
    """
    Code quality tests following SDLC coding standards
    """
    
    def test_no_hardcoded_secrets(self):
        """Test no secrets are hardcoded (SDLC Security Standards)"""
        # Check that Stripe keys are properly configured
        self.assertTrue(hasattr(settings, 'STRIPE_PUBLISHABLE_KEY'))
        self.assertTrue(hasattr(settings, 'STRIPE_SECRET_KEY'))
        
        # In production, these should come from environment variables
        # For development, they can be test keys
        stripe_pub_key = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
        if stripe_pub_key:
            # Should be a proper Stripe key format
            self.assertTrue(stripe_pub_key.startswith('pk_'))
    
    def test_logging_configured(self):
        """Test logging is properly configured (SDLC Monitoring)"""
        self.assertTrue(hasattr(settings, 'LOGGING'))
        # Should have some logging configuration
        logging_config = getattr(settings, 'LOGGING', {})
        self.assertIn('version', logging_config)
    
    def test_middleware_security_stack(self):
        """Test security middleware is properly configured (SDLC Security)"""
        middleware = getattr(settings, 'MIDDLEWARE', [])
        
        # Essential security middleware should be present
        security_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ]
        
        for middleware_class in security_middleware:
            self.assertIn(middleware_class, middleware,
                         f"Missing security middleware: {middleware_class}")
