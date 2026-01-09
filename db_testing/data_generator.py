import random
import uuid
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

EVENTS = ["view", "play", "pause", "stop"]
DEVICES = ["web", "android", "ios", "tv"]
COUNTRIES = ["US", "DE", "FR", "RU", "IN"]

def generate_batch(batch_size=10000):
    now = datetime.utcnow()
    rows = []
    for _ in range(batch_size):
        rows.append((
            now - timedelta(seconds=random.randint(0, 86400)),
            str(uuid.uuid4()),
            str(uuid.uuid4()),
            random.randint(1, 10000),
            random.choice(EVENTS),
            random.randint(0, 7200),
            random.choice(DEVICES),
            random.choice(COUNTRIES)
        ))
    return rows
