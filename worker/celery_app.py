import os
import asyncio
from celery import Celery
from simple_chalk import chalk
import service

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



# async def init_crons(sender):
#     print(chalk.green("init_crons: STARTED"))
#     tags = await service.get_all_tags()
#     print(tags)
#     every_seconds = 10
#     sender.add_periodic_task(
#         every_seconds,
#         tasks.fetch_from_yt_api.s(tags),
#     )
#     print(chalk.green("init_crons: ENDED"))

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     event_loop = asyncio.get_event_loop()
#     event_loop.run_until_complete(init_crons(sender))