import os
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
    with conn.cursor() as curr:
        curr.execute("""
        SELECT id, name, price FROM products
        """)

        product = curr.fetchone()

        print(product)
        print(product['name'])
        # Ergonomiczny Mysz v3