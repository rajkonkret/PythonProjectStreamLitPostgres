# postgres
# psycopg
# psycopg2 - starszy
# asyncpg - aplikacje asynchroniczne
# orm - mapowanie opiektowo relacyjna
# sqlalchemy

import psycopg

# ctrl / - komentarz
# pip install "psycopg[binary]"

print(psycopg.__version__)  # 3.3.6

conn = psycopg.connect(
    dbname="shop",
    user="postgres",
    password="sekret",
    host="localhost",
    port=5433
)


