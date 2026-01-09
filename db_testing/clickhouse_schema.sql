CREATE DATABASE IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.events (
    event_time     DateTime CODEC(DoubleDelta, LZ4),
    user_id        UUID,
    session_id     UUID,
    movie_id       UInt32,
    event_type     Enum8(
        'view' = 1,
        'play' = 2,
        'pause' = 3,
        'stop' = 4
    ),
    position_sec   UInt16,
    device         LowCardinality(String),
    country        FixedString(2)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(event_time)
ORDER BY (movie_id, event_time)
SETTINGS index_granularity = 8192;