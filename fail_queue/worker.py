import os
import pytz
from celery import Celery

RABBITMQ_USERNAME = os.getenv("FQ_RABBITMQ_USERNAME", "guest")
RABBITMQ_PASSWORD = os.getenv("FQ_RABBITMQ_PASSWORD", "guest")
RABBITMQ_HOST = os.getenv("FQ_RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("FQ_RABBITMQ_PORT", "5672")
REDIS_BACKEND_LINK = os.getenv("REDIS_BACKEND_LINK", "redis://localhost:6379/0")

RABBITMQ_BROKER_LINK = (
    f"amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//"
)


print(RABBITMQ_BROKER_LINK)
print(REDIS_BACKEND_LINK)


config = {
    # 'task_default_queue': "tube_failed_tasks",
    "task_routes": {
        "tube_failed_tasks": {"queue": "tube_failed_tasks"},
    },
    "timezone": pytz.timezone("UTC"),
}

worker = Celery(
    "tube_failed_tasks", broker=RABBITMQ_BROKER_LINK, backend=REDIS_BACKEND_LINK
)
worker.conf.update(**config)

# celery -A tasks worker -l info
