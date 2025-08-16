web: gunicorn ecommerce.wsgi:application --log-file -
release: python manage.py migrate
worker: celery -A ecommerce worker --loglevel=info
