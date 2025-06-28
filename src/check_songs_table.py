import duckdb
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage.db"))
print("Using database at:", db_path)

con = duckdb.connect(db_path)
try:
    result = con.execute("SELECT COUNT(*) FROM songs").fetchone()
    print(f"Number of rows in 'songs' table: {result[0]}")
except Exception as e:
    print(f"Error: {e}")
finally:
    con.close()