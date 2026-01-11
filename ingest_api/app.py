import json
import time
from gevent import monkey
monkey.patch_all()
from flask import Flask, request, jsonify
from confluent_kafka import Producer

app = Flask(__name__)

# Kafka configuration
KAFKA_CONFIG = {
    "bootstrap.servers": "kafka:9092",
    "linger.ms": 5,
    "batch.num.messages": 10000,
    "acks": "1",
}

producer = Producer(KAFKA_CONFIG)

EVENT_TOPIC_MAP = {
    "click": "events.clicks",
    "page_view": "events.page_views",
    "video": "events.video",
    "search": "events.search",
}


def delivery_report(err, msg):
    if err is not None:
        app.logger.error(f"Delivery failed: {err}")


@app.route("/ingest", methods=["POST"])
def ingest_event():
    payload = request.get_json(force=True, silent=True)

    if not payload:
        return jsonify({"error": "invalid JSON"}), 400

    event_type = payload.get("event_type")
    if event_type not in EVENT_TOPIC_MAP:
        return jsonify({"error": "unsupported event_type"}), 400

    # Enrich event
    payload["ingested_at"] = int(time.time() * 1000)
    payload["source"] = "ui"

    topic = EVENT_TOPIC_MAP[event_type]

    try:
        producer.produce(
            topic=topic,
            key=str(payload.get("user_id", "")),
            value=json.dumps(payload),
            on_delivery=delivery_report,
        )
        producer.poll(0)
    except BufferError:
        return jsonify({"error": "kafka buffer full"}), 503

    return jsonify({"status": "ok"}), 202


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
