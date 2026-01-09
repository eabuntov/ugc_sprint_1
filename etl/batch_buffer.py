import time

from event_model import Event


class EventBuffer:
    def __init__(self, max_size: int, flush_interval: int):
        self.max_size = max_size
        self.flush_interval = flush_interval
        self.buffer: list[Event] = []
        self.last_flush = time.time()

    def add(self, event: Event) -> bool:
        self.buffer.append(event)
        return self.should_flush()

    def should_flush(self) -> bool:
        return (
            len(self.buffer) >= self.max_size or
            time.time() - self.last_flush >= self.flush_interval
        )

    def flush(self) -> list[Event]:
        batch = self.buffer
        self.buffer = []
        self.last_flush = time.time()
        return batch
