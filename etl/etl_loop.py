import json
import logging

from batch_buffer import EventBuffer
from config import Settings
from event_model import Event
from external_tools import create_consumer, ClickHouseWriter


def run():
    settings = Settings()
    consumer = create_consumer(settings)
    writer = ClickHouseWriter(settings)
    buffer = EventBuffer(
        settings.batch_size,
        settings.flush_interval_sec
    )

    consumer.subscribe(settings.kafka_topics.split(","))
    try:
        while True:
            try:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    logging.error(msg.error())
                    continue

                payload = json.loads(msg.value())
                event = Event(**payload)

                if buffer.add(event):
                    batch = buffer.flush()
                    writer.insert_events(batch)
                    consumer.commit()

            except KeyboardInterrupt:
                break
    finally:
        if buffer.buffer:
            writer.insert_events(buffer.buffer)
            consumer.commit()
        consumer.close()

if __name__ == "__main__":
    run()