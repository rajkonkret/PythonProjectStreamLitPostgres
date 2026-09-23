import os
import psycopg
from dotenv import load_dotenv

# przykład transakcji na bazie danych
load_dotenv()
product_id = 1
DATABASE_URL = os.environ["DATABASE_URL"]

with psycopg.connect(DATABASE_URL) as conn:
    with conn.transaction():
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE products
                SET quantity = quantity
                WHERE id = %s
                    AND quantity > 0
                    RETURNING id
                    """,
                (product_id,)
            )

            product = cur.fetchone()

            if product is None:
                raise ValueError("Brak produktu.")

            cur.execute(
                """
                INSERT INTO orders (product_id)
                VALUES (%s)
                """,
                (product_id,)
            )
