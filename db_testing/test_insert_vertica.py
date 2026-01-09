import time
import vertica_python
from data_generator import generate_batch


conn = vertica_python.connect(
    host="localhost",
    port=5433,
    user="dbadmin",
    password="dbadmin",
    database="analytics"
)
cur = conn.cursor()

rows = generate_batch(1_000_000)

start = time.time()
cur.executemany("""
    INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", rows)
conn.commit()

print("Vertica insert time:", time.time() - start)
