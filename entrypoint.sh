#!/bin/sh
set -e

# Ensure we're in the correct working directory
cd /opt/render/project/src

# Apply any pending migrations (will create SQLite DB in runtime path)
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start the application
exec gunicorn Promt.wsgi:application --config gunicorn.conf.py
