import os
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg.connect[DATABASE_URL]

cur = conn.cursor()