#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate

echo "Creating staticfiles directory..."
mkdir -p staticfiles

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || echo "Warning: collectstatic failed, continuing anyway..."

echo "Starting gunicorn..."
exec gunicorn core.wsgi --bind 0.0.0.0:$PORT

