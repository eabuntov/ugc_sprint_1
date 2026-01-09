import time
import vertica_python

conn = vertica_python.connect(
    host="localhost",
    port=5433,
    user="dbadmin",
    password="dbadmin",
    database="analytics"
)

cur = conn.cursor()

queries = [
    """SELECT
    movie_id,
    DATE_TRUNC('hour', event_time) AS hour,
    COUNT(*)
    FROM events
    GROUP BY movie_id, hour
    ORDER BY hour DESC
    LIMIT 100;
    """,
    """SELECT
    movie_id,
    COUNT(DISTINCT user_id)
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
        cur.execute(query)
        times.append(time.time() - start)
    return sum(times) / runs

if __name__ == '__main__':
    print(benchmark(queries[0]))
    print(benchmark(queries[1]))