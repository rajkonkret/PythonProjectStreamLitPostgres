import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg.connect(DATABASE_URL)

with conn.cursor() as cur:
    cur.execute("SELECT version()")
    print(cur.fetchone())

# bardziej eleganckie
with psycopg.connect(DATABASE_URL)  as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version()")
        print(cur.fetchone())