import logging
import redis
import sys
import os
from datetime import datetime, timedelta

log = logging.getLogger("tube_api")
log.setLevel(logging.INFO)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)


def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            socket_timeout=5,
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError as e:
        log.error("Redis AuthenticationError: " + str(e))
        sys.exit(1)


def get_tag_results_from_cache(key: str) -> str:
    val = client.get(key)
    return val


def set_tag_results_to_cache(key: str, value: str) -> bool:
    state = client.setex(
        key,
        timedelta(seconds=3600),
        value=value,
    )
    return state


client = redis_connect()
