import os
from celery import Celery

BROKER_LINK = os.environ.get("BROKER_LINK", "amqp://guest@localhost//")

config = {
    # 'task_default_queue': "tube_query_celery",
    'task_routes': {
        'tube_query_celery': {'queue': 'tube_query_celery'},
        'tube_crud_celery': {'queue': 'tube_crud_celery'},
    }
    # 'enable_utc': True,
}

# TODO: Add a backend link to the config
app = Celery('tube_main', broker=BROKER_LINK)
app.conf.update(**config)

# celery -A tasks worker -l info