# Riya Group E-commerce Platform - Production Deployment Guide

## 🚀 Production Deployment Checklist

### Prerequisites
- [ ] Python 3.12+
- [ ] PostgreSQL 14+ (or compatible database)
- [ ] Redis 6+ (for caching and sessions)
- [ ] Nginx/Apache (web server)
- [ ] SSL Certificate
- [ ] Domain name configured

### Environment Setup

1. **Clone the repository and install dependencies:**
```bash
git clone <your-repo-url>
cd ecommerce
pip install -r requirements.txt
```

2. **Set up environment variables:**
Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

Edit `.env` with your production values:
```env
DEBUG=False
SECRET_KEY=your_very_secure_secret_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/riyagroup_db
ALLOWED_HOST=riyagroup.com

# Stripe (production keys)
STRIPE_PUBLISHABLE_KEY=pk_live_your_live_key
STRIPE_SECRET_KEY=sk_live_your_live_key

# Email (SMTP configuration)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@riyagroup.com
EMAIL_HOST_PASSWORD=your_email_password

# Cache/Session
REDIS_URL=redis://localhost:6379/1

# AWS S3 (optional, for media files)
USE_S3=TRUE
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_STORAGE_BUCKET_NAME=riyagroup-media

# Error tracking (optional)
SENTRY_DSN=https://your-sentry-dsn
```

### Database Setup

1. **Create PostgreSQL database:**
```sql
CREATE DATABASE riyagroup_db;
CREATE USER riyagroup_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE riyagroup_db TO riyagroup_user;
```

2. **Run migrations:**
```bash
python manage.py migrate
```

3. **Create superuser:**
```bash
python manage.py createsuperuser
```

4. **Load sample data (optional):**
```bash
python manage.py populate_data
```

### Static Files and Media

1. **Collect static files:**
```bash
python manage.py collectstatic --noinput
```

2. **Compress static files:**
```bash
python manage.py compress --force
```

### Security Configuration

1. **Run security check:**
```bash
python manage.py check --deploy
```

2. **Ensure SSL is configured:**
- Set up SSL certificates
- Configure HTTPS redirect
- Update ALLOWED_HOSTS

### Web Server Configuration

#### Nginx Configuration Example:
```nginx
server {
    listen 80;
    server_name riyagroup.com www.riyagroup.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name riyagroup.com www.riyagroup.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    location /static/ {
        alias /path/to/your/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /path/to/your/media/;
        expires 1y;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Application Server

#### Using Gunicorn:
```bash
gunicorn ecommerce.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log
```

#### Systemd Service (Linux):
Create `/etc/systemd/system/riyagroup.service`:
```ini
[Unit]
Description=Riya Group E-commerce
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/ecommerce
Environment="DJANGO_SETTINGS_MODULE=ecommerce.settings.production"
ExecStart=/path/to/your/venv/bin/gunicorn ecommerce.wsgi:application --bind unix:/run/gunicorn.sock
Restart=always

[Install]
WantedBy=multi-user.target
```

### Background Tasks (Celery)

1. **Start Celery worker:**
```bash
celery -A ecommerce worker --loglevel=info
```

2. **Start Celery beat (for scheduled tasks):**
```bash
celery -A ecommerce beat --loglevel=info
```

### Monitoring and Logging

1. **Log files location:** `/path/to/your/logs/`
2. **Monitor with Sentry:** Configure SENTRY_DSN in environment
3. **Database monitoring:** Set up PostgreSQL monitoring
4. **Redis monitoring:** Monitor cache performance

### Backup Strategy

1. **Database backups:**
```bash
pg_dump riyagroup_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

2. **Media files backup:**
```bash
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/
```

### Performance Optimization

1. **Enable database connection pooling**
2. **Configure Redis for caching**
3. **Use CDN for static files**
4. **Enable Gzip compression**
5. **Optimize database queries**

### Security Best Practices

- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS everywhere
- [ ] Configure CSRF protection
- [ ] Set secure cookie flags
- [ ] Use security headers
- [ ] Regular security updates
- [ ] Monitor for suspicious activity
- [ ] Backup encryption

### Testing in Production

1. **Smoke tests:**
```bash
python manage.py check
python manage.py test --keepdb
```

2. **Load testing:**
- Test with realistic user loads
- Monitor response times
- Check database performance

### Troubleshooting

**Common issues:**
1. Static files not loading → Check STATIC_ROOT and web server config
2. Database connection errors → Verify DATABASE_URL and credentials
3. 500 errors → Check logs in `/logs/django_errors.log`
4. Cache issues → Verify Redis connection

**Log locations:**
- Application logs: `/logs/django.log`
- Error logs: `/logs/django_errors.log`
- Web server logs: `/var/log/nginx/` (or Apache equivalent)

### Maintenance

1. **Regular updates:**
```bash
pip install -r requirements.txt --upgrade
python manage.py migrate
python manage.py collectstatic --noinput
```

2. **Database maintenance:**
```bash
python manage.py clearsessions  # Clear expired sessions
python manage.py cleanup_uploads  # Clean orphaned files
```

---

## 🎯 Quick Production Setup

For a quick production setup, run:
```bash
chmod +x deploy.sh
./deploy.sh
```

Or on Windows:
```powershell
.\deploy.ps1
```

This will automatically set up your production environment with all necessary configurations.

---

**Support:** For issues or questions, contact the development team or check the documentation.
**Version:** 1.0.0
**Last Updated:** June 2025
