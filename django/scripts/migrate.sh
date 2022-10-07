#!/bin/bash
set -e

echo 'INFO: Migration started...'

python ../manage.py makemigrations
python ../manage.py migrate

echo 'INFO: Done'
