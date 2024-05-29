#!/bin/sh

echo 'Waiting for postgres...'


echo 'PostgreSQL started'

echo 'Running migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input
python manage.py initadmin

echo 'Starting Gunicorn...'
# Modify this command to start Gunicorn with appropriate settings
# Example: gunicorn config.wsgi:application --bind 0.0.0.0:8000
# Replace 'config.wsgi:application' with your actual WSGI application entry point
# Replace '0.0.0.0:8000' with the appropriate host and port
gunicorn --timeout 500 config.wsgi:application

exec "$@"
