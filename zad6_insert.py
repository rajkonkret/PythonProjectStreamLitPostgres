import os
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg.connect(DATABASE_URL)

cur = conn.cursor()

# CRUD

cur.execute(
    """
    INSERT INTO products (name, price, quantity)
    VALUES (%s, %s, %s)
    """,
    ("Laptop", 3999.99, 5)
)

conn.commit()

# RETURNING
cur.execute(
    """
    INSERT INTO products (name, price, quantity)
    VALUES (%s, %s, %s)
    RETURNING id, name, price, quantity
    """,
    ("Laptop", 3999.99, 5)
)
product = cur.fetchone()

print(product)
# (108, 'Laptop', Decimal('3999.99'), 5)

name = "Laptop"

# cur.execute(
#     f"SELECT * FROM products WHERE name='{name}'"
# )

cur.execute(
    """
    SELECT *
    FROM products
    WHERE name = %s
    """,
    (name,)
)
product = cur.fetchone()

print(product)

conn.commit()
conn.close()
