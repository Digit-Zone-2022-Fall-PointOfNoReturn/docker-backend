import os
import sys

import psycopg2


try:
    conn = psycopg2.connect(
        dbname=os.environ['DJANGO_POSTGRES_DB'],
        user=os.environ['DJANGO_POSTGRES_USER'],
        password=os.environ['DJANGO_POSTGRES_PASSWORD'],
        host=os.environ['DJANGO_POSTGRES_HOST'],
        port=os.environ['DJANGO_POSTGRES_PORT']
    )

    with conn.cursor() as cur:
        cur.execute("SELECT 1;")
        cur.fetchone()

# No need to log, this is help script that must be used only as test
except Exception:
    sys.exit(-1)
