#!/bin/bash

echo "Starting Django deployment..."

run_migrations() {
    app_name=$1
    echo "Running migrations for $app_name..."
    python manage.py makemigrations $app_name --noinput || exit 1
    python manage.py migrate $app_name --noinput || exit 1
    return 0
}

check_migrations() {
    python manage.py showmigrations | grep -q "\[ \]"
    return $?
}

# Clear any pending migrations first
echo "Checking for conflicting migrations..."
python manage.py migrate --fake-initial

# Run migrations in dependency order
echo "Running migrations in order..."

# Base apps (no dependencies)
run_migrations "authentication"
run_migrations "myadmin"
run_migrations "customer"

# Final migration check
echo "Running any remaining migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Creating cache tables..."
python manage.py createcachetable 

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn in the background
echo "Starting Gunicorn..."
gunicorn graduation_backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info &

# Start Daphne for WebSocket connections
echo "Starting Daphne..."
daphne -p 8001 graduation_backend.asgi:application --bind 0.0.0.0