from confluent_kafka import Consumer
from clickhouse_driver import Client

from config import Settings
from event_model import Event


def create_consumer(settings: Settings) -> Consumer:
    return Consumer({
        "bootstrap.servers": settings.kafka_bootstrap_servers,
        "group.id": settings.kafka_group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
        "max.poll.interval.ms": 300_000
    })


class ClickHouseWriter:
    def __init__(self, settings):
        self.client = Client(
            host=settings.clickhouse_host,
            database=settings.clickhouse_database,
            user=settings.clickhouse_user,
            password=settings.clickhouse_password
        )

    def insert_events(self, events: list[Event]):
        data = [
            (
                e.event_id,
                e.event_date,
                e.event_time,
                e.event_type,
                e.user_id,
                e.session_id,
                e.page_url,
                e.element_id,
                e.metadata,
            )
            for e in events
        ]

        self.client.execute(
            """
            INSERT INTO events_raw (
                event_id, event_date, event_time,
                event_type, user_id, session_id,
                page_url, element_id, metadata
            ) VALUES
            """,
            data
        )

