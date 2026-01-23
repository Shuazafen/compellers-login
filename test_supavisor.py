import os
import sys

# Add PostgreSQL DLL directory on Windows
if os.name == 'nt':
    pg_bin = r"C:\Program Files\PostgreSQL\18\bin"
    if os.path.exists(pg_bin):
        os.add_dll_directory(pg_bin)
        os.environ["PATH"] = pg_bin + os.pathsep + os.environ["PATH"]

import psycopg
from urllib.parse import quote_plus

USER = 'postgres.bqyujhcttkvulrnmhmxn'
PASS = '1986@olA12=1'
HOST = '127.0.0.1'
PORT = 5433
DB = 'postgres'

print(f"Testing connection to {HOST}:{PORT}...")

password_enc = quote_plus(PASS)
# Try both standard and unencoded (just in case)
conn_str = f"postgresql://{USER}:{password_enc}@{HOST}:{PORT}/{DB}?sslmode=require"

print(f"Connection string: postgresql://{USER}:****@{HOST}:{PORT}/{DB}?sslmode=require")

try:
    conn = psycopg.connect(conn_str, connect_timeout=10)
    print("SUCCESS: Connected!")
    conn.close()
except Exception as e:
    print(f"FAILURE: {type(e).__name__}: {e}")
