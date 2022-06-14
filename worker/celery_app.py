import os
import pytz
from celery import Celery

RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")

RABBITMQ_BROKER_LINK = (
    f"amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//"
)


config = {
    # 'task_default_queue': "tube_query_celery",
    "task_routes": {
        "tube_query_celery": {"queue": "tube_query_celery"},
        "tube_crud_celery": {"queue": "tube_crud_celery"},
    },
    "timezone": pytz.timezone("UTC"),
}

# TODO: Add a backend link to the config
app = Celery("tube_main", broker=RABBITMQ_BROKER_LINK)
app.conf.update(**config)

# celery -A tasks worker -l info
