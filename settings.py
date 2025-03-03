from typing import Optional

from pydantic import BaseSettings
from functools import lru_cache


class MqttSettings(BaseSettings):
    class Config:
        env_file = '.env'
        env_prefix = 'mqtt_'

    host: str = "localhost"
    port: int = 1883
    topic: str = "sensors"
    username: Optional[str]
    password: Optional[str]


class MongoSettings(BaseSettings):
    # TODO: mask username and password
    username: str = "root"
    password: str = "rootpassword"
    port: int = 27017
    uri: str = f"mongodb://{username}:{password}@mongo:{port}/"
    db_name: str = "sensors_db"
    collection_name: str = "sensors_data"


class PostgresSettings(BaseSettings):
    username: str = "root"
    password: str = "rootpassword"
    db_name: str = "data_warehouse"
    port: int = 5432


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    mqtt: MqttSettings = MqttSettings()
    mongo: MongoSettings = MongoSettings()
    postgres: PostgresSettings = PostgresSettings()
    interval_ms: int = 1000
    logging_level: int = 30


@lru_cache()
def get_settings() -> Settings:
    return Settings()
