#!/bin/bash

wait-for-it $DB_HOST:$DB_PORT

python manage.py collectstatic --noinput &
# NOTE: We will only migrate data in django migration
# Don't use default schmea for migrations
python manage.py migrate --database=default &
./manage.py run_celery_dev &
python manage.py runserver 0.0.0.0:7020
