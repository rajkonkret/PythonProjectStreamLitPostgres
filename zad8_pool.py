import os
import time
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

# 1. Konfiguracja połączenia do bazy 'shop'
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "shop")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "sekret")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 2. Inicjalizacja puli połączeń
# kwargs={'row_factory': dict_row} sprawia, że wyniki zapytań to słowniki: {'id': 1, 'name': '...'}
pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=2,          # Zawsze 2 gotowe połączenia w pamięci
    max_size=5,          # Maksymalnie 5 połączeń w szczycie
    max_idle=300.0,      # Zamknij nadmiarowe połączenia po 5 minutach bezczynności
    kwargs={"row_factory": dict_row},
)


# -------------------------------------------------------------
# Funkcje biznesowe operujące na puli
# -------------------------------------------------------------

def get_top_expensive_products(limit: int = 5):
    """Pobieranie danych z bazy (SELECT) przez wypożyczone połączenie."""
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, price, quantity 
                FROM products 
                ORDER BY price DESC 
                LIMIT %s;
            """, (limit,))
            return cur.fetchall()


def update_product_stock(product_id: int, quantity_change: int):
    """Modyfikacja stanu magazynowego z automatyczną transakcją."""
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # Sprawdzenie obecnego stanu
            cur.execute("SELECT name, quantity FROM products WHERE id = %s;", (product_id,))
            prod = cur.fetchone()
            if not prod:
                print(f"[Ostrzeżenie] Brak produktu o ID {product_id}")
                return

            new_qty = prod["quantity"] + quantity_change
            if new_qty < 0:
                # Wyrzucenie wyjątku wewnątrz bloku spowoduje automatyczny ROLLBACK
                raise ValueError(f"Brak wystarczającej liczby sztuk dla '{prod['name']}'! Stan: {prod['quantity']}")

            cur.execute("""
                UPDATE products 
                SET quantity = %s 
                WHERE id = %s;
            """, (new_qty, product_id))

            print(f"[OK] Zaktualizowano '{prod['name']}': {prod['quantity']} -> {new_qty} szt.")
        # Po wyjściu z 'with pool.connection()' następuje automatyczny COMMIT


def simulate_client(client_id: int):
    """Symulacja pojedynczego wątku / klienta odpytującego bazę."""
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # Każde fizyczne połączenie ma swój identyfikator pg_backend_pid()
            cur.execute("SELECT pg_backend_pid(), count(*) as total FROM products;")
            row = cur.fetchone()
            print(f"Klient {client_id:<2} obsłużony przez Postgres PID {row['pg_backend_pid']} (znaleziono {row['total']} produktów)")
            time.sleep(0.05)  # Drobna symulacja pracy


# -------------------------------------------------------------
# Główny blok demonstracyjny
# -------------------------------------------------------------

def main():
    print("=== 1. Odczyt danych z użyciem ConnectionPool ===")
    top_products = get_top_expensive_products(3)
    for p in top_products:
        print(f"Produkt: {p['name']:<30} | Cena: {p['price']:>8} PLN | Stan: {p['quantity']}")

    print("\n=== 2. Aktualizacja stanu w transakcji ===")
    if top_products:
        pierwszy_id = top_products[0]["id"]
        update_product_stock(pierwszy_id, 5)

    print("\n=== 3. Symulacja 12 równoległych żądań na puli max_size=5 ===")
    print("(Zauważ, że tylko 5 procesów Postgresa PID obsłuży wszystkich 12 klientów)")
    with ThreadPoolExecutor(max_workers=8) as executor:
        for i in range(1, 13):
            executor.submit(simulate_client, i)

    # Grzeczne zamknięcie puli przy zatrzymywaniu programu/aplikacji
    pool.close()
    print("\nPula połączeń została zamknięta.")


if __name__ == "__main__":
    main()
