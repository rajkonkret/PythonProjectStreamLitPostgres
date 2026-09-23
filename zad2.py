import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

try:
    conn = psycopg.connect(DATABASE_URL)

    cur = conn.cursor()

    cur.execute(
        "SELECT version()"
    )

    print(cur.fetchone())
except Exception as e:
    print(e)
finally:
    cur.close()
    conn.close()