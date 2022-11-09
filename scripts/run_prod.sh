#!/bin/bash
python manage.py collectstatic --noinput &
python manage.py migrate --noinput &
# start server
gunicorn config.wsgi:application --timeout=40 --bind 0.0.0.0:7020 &
# FIXME: run this separately celery
celery -A config worker --loglevel=INFO
