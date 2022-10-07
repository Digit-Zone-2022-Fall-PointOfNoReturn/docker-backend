#!/bin/bash
set -e

echo 'INFO: Starting collect static...'

python ../manage.py collectstatic --no-input

echo 'INFO: Done'
