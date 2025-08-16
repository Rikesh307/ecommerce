// Enhanced Riya Group E-commerce JavaScript
// Performance and functionality improvements

// Utility Functions
class RiyaGroupUtils {
    static getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    static showNotification(message, type = 'success', duration = 3000) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 1060;
            min-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
            </div>
        `;

        document.body.appendChild(notification);

        // Auto-remove after duration
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, duration);
    }

    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    static formatPrice(price) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(price);
    }

    static animateCount(element, target, duration = 1000) {
        const start = parseInt(element.textContent) || 0;
        const increment = (target - start) / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= target) || (increment < 0 && current <= target)) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 16);
    }
}

// Enhanced Search Functionality
class SearchManager {
    constructor() {
        this.searchInput = document.getElementById('search-input');
        this.searchSuggestions = document.getElementById('search-suggestions');
        this.searchLoading = document.getElementById('search-loading');
        this.selectedCategory = '';
        
        this.init();
    }

    init() {
        if (!this.searchInput) return;

        // Debounced search for better performance
        const debouncedSearch = RiyaGroupUtils.debounce((query) => {
            this.performSearch(query);
        }, 300);

        this.searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            if (query.length >= 2) {
                this.showLoading(true);
                debouncedSearch(query);
            } else {
                this.hideSuggestions();
            }
        });

        // Handle category selection
        document.querySelectorAll('[data-category]').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.selectedCategory = e.target.dataset.category;
                document.getElementById('selected-category').textContent = e.target.textContent;
            });
        });

        // Hide suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.search-container')) {
                this.hideSuggestions();
            }
        });
    }

    async performSearch(query) {
        try {
            const url = new URL('/products/api/search-suggestions/', window.location.origin);
            url.searchParams.append('q', query);
            if (this.selectedCategory) {
                url.searchParams.append('category', this.selectedCategory);
            }

            const response = await fetch(url);
            const data = await response.json();
            
            this.showSuggestions(data.suggestions);
        } catch (error) {
            console.error('Search error:', error);
            this.hideSuggestions();
        } finally {
            this.showLoading(false);
        }
    }

    showSuggestions(suggestions) {
        if (!this.searchSuggestions) return;

        if (suggestions.length === 0) {
            this.hideSuggestions();
            return;
        }

        const html = suggestions.map(suggestion => `
            <li>
                <a class="dropdown-item d-flex align-items-center" href="${suggestion.url}">
                    <i class="bi bi-search me-2 text-muted"></i>
                    <span>${suggestion.name}</span>
                </a>
            </li>
        `).join('');

        this.searchSuggestions.innerHTML = html;
        this.searchSuggestions.classList.add('show');
    }

    hideSuggestions() {
        if (this.searchSuggestions) {
            this.searchSuggestions.classList.remove('show');
        }
    }

    showLoading(show) {
        if (this.searchLoading) {
            this.searchLoading.classList.toggle('d-none', !show);
        }
    }
}

// Cart Management
class CartManager {
    constructor() {
        this.cartCount = document.getElementById('cart-count');
        this.init();
    }

    init() {
        // Initialize cart event listeners
        document.addEventListener('click', (e) => {
            if (e.target.closest('.btn-add-cart')) {
                e.preventDefault();
                const productId = e.target.closest('.btn-add-cart').dataset.productId;
                if (productId) {
                    this.addToCart(productId);
                }
            }
        });
    }

    async addToCart(productId, quantity = 1) {
        const button = document.querySelector(`[data-product-id="${productId}"]`);
        const originalContent = button.innerHTML;
        
        try {
            // Show loading state
            button.disabled = true;
            button.innerHTML = '<i class="spinner-border spinner-border-sm me-2"></i>Adding...';

            const response = await fetch(`/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': RiyaGroupUtils.getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ quantity })
            });

            const data = await response.json();

            if (data.success) {
                RiyaGroupUtils.showNotification('Product added to cart!', 'success');
                this.updateCartCount(data.cart_count);
                this.animateCartIcon();
            } else {
                throw new Error(data.message || 'Failed to add to cart');
            }
        } catch (error) {
            RiyaGroupUtils.showNotification(error.message || 'Error adding to cart', 'danger');
        } finally {
            // Restore button state
            button.disabled = false;
            button.innerHTML = originalContent;
        }
    }

    updateCartCount(count) {
        if (this.cartCount) {
            const currentCount = parseInt(this.cartCount.textContent) || 0;
            if (count !== currentCount) {
                RiyaGroupUtils.animateCount(this.cartCount, count);
            }
        }

        // Update all cart count elements
        document.querySelectorAll('.cart-count, [data-cart-count]').forEach(element => {
            element.textContent = count;
        });
    }

    animateCartIcon() {
        const cartIcon = document.querySelector('.cart-icon, .bi-cart3');
        if (cartIcon) {
            cartIcon.style.transform = 'scale(1.2)';
            cartIcon.style.color = 'var(--success)';
            
            setTimeout(() => {
                cartIcon.style.transform = 'scale(1)';
                cartIcon.style.color = '';
            }, 300);
        }
    }
}

// Wishlist Management
class WishlistManager {
    constructor() {
        this.init();
    }

    init() {
        document.addEventListener('click', (e) => {
            if (e.target.closest('.btn-wishlist')) {
                e.preventDefault();
                const productId = e.target.closest('.btn-wishlist').dataset.productId;
                if (productId) {
                    this.toggleWishlist(productId);
                }
            }
        });
    }

    async toggleWishlist(productId) {
        const button = document.querySelector(`[data-product-id="${productId}"].btn-wishlist`);
        const icon = button.querySelector('i');
        const isInWishlist = button.classList.contains('active');

        try {
            const response = await fetch(`/products/wishlist/toggle/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': RiyaGroupUtils.getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (data.success) {
                if (data.in_wishlist) {
                    button.classList.add('active');
                    icon.className = 'bi bi-heart-fill';
                    RiyaGroupUtils.showNotification('Added to wishlist!', 'success');
                } else {
                    button.classList.remove('active');
                    icon.className = 'bi bi-heart';
                    RiyaGroupUtils.showNotification('Removed from wishlist', 'info');
                }
                
                // Animate the heart
                icon.style.transform = 'scale(1.3)';
                setTimeout(() => {
                    icon.style.transform = 'scale(1)';
                }, 200);
            } else {
                throw new Error(data.message || 'Failed to update wishlist');
            }
        } catch (error) {
            RiyaGroupUtils.showNotification(error.message || 'Error updating wishlist', 'danger');
        }
    }
}

// Image Gallery and Zoom
class ImageGallery {
    constructor() {
        this.mainImage = document.getElementById('mainImage');
        this.thumbnails = document.querySelectorAll('.thumbnail');
        this.init();
    }

    init() {
        if (!this.mainImage) return;

        // Thumbnail click handlers
        this.thumbnails.forEach((thumbnail, index) => {
            thumbnail.addEventListener('click', () => {
                this.changeMainImage(thumbnail.src, index);
            });

            // Keyboard navigation
            thumbnail.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.changeMainImage(thumbnail.src, index);
                }
            });
        });

        // Image zoom on hover
        this.mainImage.addEventListener('mouseenter', () => {
            this.enableZoom();
        });

        this.mainImage.addEventListener('mouseleave', () => {
            this.disableZoom();
        });
    }

    changeMainImage(src, index) {
        // Smooth transition
        this.mainImage.style.opacity = '0.7';
        
        setTimeout(() => {
            this.mainImage.src = src;
            this.mainImage.style.opacity = '1';
        }, 150);

        // Update active thumbnail
        this.thumbnails.forEach(thumb => thumb.classList.remove('active'));
        if (this.thumbnails[index]) {
            this.thumbnails[index].classList.add('active');
        }
    }

    enableZoom() {
        this.mainImage.style.cursor = 'zoom-in';
        this.mainImage.style.transform = 'scale(1.05)';
    }

    disableZoom() {
        this.mainImage.style.cursor = 'default';
        this.mainImage.style.transform = 'scale(1)';
    }
}

// Location Manager
class LocationManager {
    constructor() {
        this.currentLocation = document.getElementById('current-location');
        this.locationModal = document.getElementById('locationModal');
        this.init();
    }

    init() {
        // Load saved location
        const savedLocation = localStorage.getItem('selectedLocation') || 'Nepal';
        this.updateLocation(savedLocation);
    }

    updateLocation(location) {
        if (this.currentLocation) {
            this.currentLocation.textContent = location;
            localStorage.setItem('selectedLocation', location);
        }
        
        // Close modal if open
        if (this.locationModal) {
            const modal = bootstrap.Modal.getInstance(this.locationModal);
            if (modal) modal.hide();
        }
        
        RiyaGroupUtils.showNotification(`Delivery location updated to ${location}`, 'info');
    }
}

// Performance Monitoring
class PerformanceMonitor {
    constructor() {
        this.init();
    }

    init() {
        // Monitor page load performance
        window.addEventListener('load', () => {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                this.logPerformanceMetrics(perfData);
            }
        });

        // Monitor LCP (Largest Contentful Paint)
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                console.log('LCP:', lastEntry.startTime);
            });
            observer.observe({ entryTypes: ['largest-contentful-paint'] });
        }
    }

    logPerformanceMetrics(perfData) {
        const metrics = {
            'DNS Lookup': perfData.domainLookupEnd - perfData.domainLookupStart,
            'TCP Connection': perfData.connectEnd - perfData.connectStart,
            'Request Time': perfData.responseStart - perfData.requestStart,
            'Response Time': perfData.responseEnd - perfData.responseStart,
            'DOM Processing': perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
            'Total Load Time': perfData.loadEventEnd - perfData.navigationStart
        };

        console.group('🚀 Riya Group Performance Metrics');
        Object.entries(metrics).forEach(([key, value]) => {
            const color = value > 1000 ? 'color: red' : value > 500 ? 'color: orange' : 'color: green';
            console.log(`%c${key}: ${Math.round(value)}ms`, color);
        });
        console.groupEnd();

        // Warn about slow performance
        if (metrics['Total Load Time'] > 3000) {
            console.warn('⚠️ Page load time exceeds 3 seconds. Consider optimization.');
        }
    }
}

// Progressive Web App features
class PWAManager {
    constructor() {
        this.deferredPrompt = null;
        this.init();
    }

    init() {
        // Listen for install prompt
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            this.deferredPrompt = e;
            this.showInstallButton();
        });

        // Handle install click
        document.addEventListener('click', (e) => {
            if (e.target.id === 'installApp') {
                this.installApp();
            }
        });
    }

    showInstallButton() {
        // Create install button if it doesn't exist
        let installBtn = document.getElementById('installApp');
        if (!installBtn) {
            installBtn = document.createElement('button');
            installBtn.id = 'installApp';
            installBtn.className = 'btn btn-outline-primary btn-sm position-fixed';
            installBtn.style.cssText = 'bottom: 20px; left: 20px; z-index: 1050;';
            installBtn.innerHTML = '<i class="bi bi-download me-2"></i>Install App';
            document.body.appendChild(installBtn);
        }
    }

    async installApp() {
        if (!this.deferredPrompt) return;

        this.deferredPrompt.prompt();
        const { outcome } = await this.deferredPrompt.userChoice;
        
        if (outcome === 'accepted') {
            RiyaGroupUtils.showNotification('App installed successfully!', 'success');
        }
        
        this.deferredPrompt = null;
        document.getElementById('installApp')?.remove();
    }
}

// Global functions for backward compatibility
window.showLocationModal = function() {
    const modal = new bootstrap.Modal(document.getElementById('locationModal'));
    modal.show();
};

window.selectLocation = function(location) {
    window.locationManager.updateLocation(location);
};

window.performSearch = function() {
    const searchInput = document.getElementById('search-input');
    const query = searchInput.value.trim();
    if (query) {
        const category = window.searchManager?.selectedCategory || '';
        const url = new URL('/products/', window.location.origin);
        url.searchParams.append('q', query);
        if (category) url.searchParams.append('category', category);
        window.location.href = url.toString();
    }
};

// Initialize all managers when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    window.searchManager = new SearchManager();
    window.cartManager = new CartManager();
    window.wishlistManager = new WishlistManager();
    window.imageGallery = new ImageGallery();
    window.locationManager = new LocationManager();
    window.performanceMonitor = new PerformanceMonitor();
    window.pwaManager = new PWAManager();

    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Add loading states to all buttons
    document.querySelectorAll('button[type="submit"]').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.disabled) {
                this.classList.add('btn-loading');
                setTimeout(() => {
                    this.classList.remove('btn-loading');
                }, 2000);
            }
        });
    });

    // Console welcome message
    console.log('%c🛍️ Welcome to Riya Group E-commerce!', 'color: #0ea5e9; font-size: 16px; font-weight: bold;');
    console.log('%cBuilt with performance and user experience in mind.', 'color: #64748b; font-size: 12px;');
});
