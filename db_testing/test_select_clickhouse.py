import time

import clickhouse_connect

client = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    username="test",
    password="test",
    database="analytics"
)

queries = [
    """SELECT
    movie_id,
    toStartOfHour(event_time) AS hour,
    count()
    FROM events
    GROUP BY movie_id, hour
    ORDER BY hour DESC
    LIMIT 100;
    """,
    """SELECT
    movie_id,
    uniqExact(user_id)
    FROM events
    GROUP BY movie_id
    ORDER BY 2 DESC
    LIMIT 10;
    """,

]

def benchmark(query, runs=5):
    times = []
    for _ in range(runs):
        start = time.time()
        client.query(query)
        times.append(time.time() - start)
    return sum(times) / runs

if __name__ == '__main__':
    print(benchmark(queries[0]))
    print(benchmark(queries[1]))