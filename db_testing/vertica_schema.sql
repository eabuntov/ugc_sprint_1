CREATE TABLE events (
    event_time     TIMESTAMP NOT NULL,
    user_id        UUID NOT NULL,
    session_id     UUID NOT NULL,
    movie_id       INT NOT NULL,
    event_type     VARCHAR(10) NOT NULL,
    position_sec   SMALLINT,
    device         VARCHAR(32),
    country        CHAR(2)
)
SEGMENTED BY HASH(user_id) ALL NODES
ORDER BY event_time;