from pydantic import BaseSettings

class Settings(BaseSettings):
    kafka_bootstrap_servers: str
    kafka_group_id: str
    kafka_topics: list[str]

    clickhouse_host: str
    clickhouse_database: str
    clickhouse_user: str
    clickhouse_password: str

    batch_size: int = 5_000
    flush_interval_sec: int = 5

    class Config:
        env_file = ".env"
