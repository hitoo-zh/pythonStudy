#!/bin/bash

# Start the Django application with Docker Compose
echo "Starting Django Demo Application..."

# Build and start all services
docker-compose up --build -d

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run migrations
echo "Running database migrations..."
docker-compose exec web python manage.py migrate

# Create superuser (optional)
echo "Creating superuser..."
docker-compose exec web python manage.py createsuperuser --noinput --username admin --email admin@example.com || echo "Superuser creation skipped (may already exist)"

# Collect static files
echo "Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

echo "Application started successfully!"
echo "Access the application at: http://localhost:8000"
echo "Admin panel: http://localhost:8000/admin/"
echo "API documentation: http://localhost:8000/api/"