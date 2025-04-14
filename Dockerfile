# Dockerfile

# Use the official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (optional if you use static)
RUN python manage.py collectstatic --noinput

# Run Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
