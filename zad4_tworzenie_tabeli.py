import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg.connect(DATABASE_URL)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
price NUMERIC(10, 2),
quantity INTEGER
)
""")

conn.commit()

cur.execute("""
SELECT id, name, price FROM products
""")

row = cur.fetchone()

print(row)
conn.close()
# (1, 'Ergonomiczny Mysz v3', Decimal('627.08'))