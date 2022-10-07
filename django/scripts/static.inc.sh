#!/bin/bash
set -e

echo 'INFO: Starting collect static...'

python "${PARENT?error}/manage.py" collectstatic --no-input

echo 'INFO: Done'
