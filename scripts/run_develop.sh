#!/bin/bash

python manage.py collectstatic --noinput &
# NOTE: We will only migrate data in django migration
# Don't use default schmea for migrations
python manage.py migrate --database=django &
python manage.py runserver 0.0.0.0:7020
