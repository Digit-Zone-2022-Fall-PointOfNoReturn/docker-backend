#!/bin/bash
set -e

echo 'INFO: Migration started...'

python "${PARENT?error}/manage.py" makemigrations
python "${PARENT?error}/manage.py" migrate

echo 'INFO: Done'
