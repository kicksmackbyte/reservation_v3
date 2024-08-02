#!/bin/sh
python manage.py collectstatic --no-input --clear
python manage.py migrate
gunicorn reservation.wsgi --name reservation-service --workers 3 --timeout 60 --bind 0.0.0.0:8000
exec "$@"
