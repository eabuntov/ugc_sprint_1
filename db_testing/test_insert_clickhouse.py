import clickhouse_connect
from .data_generator import generate_batch
import time

client = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    username="test",
    password="test",
    database="analytics"
)

rows = generate_batch(1_000_000)

start = time.time()
client.insert(
    "events",
    rows,
    column_names=[
        "event_time", "user_id", "session_id",
        "movie_id", "event_type",
        "position_sec", "device", "country"
    ]
)
print("ClickHouse insert time:", time.time() - start)
