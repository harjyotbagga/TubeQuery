import asyncio
import logging
import queue
from simple_chalk import chalk
import tasks, service
from celery_app import app

logger = logging.getLogger("tube_beat")
logger.setLevel(logging.INFO)

# celery -A celery_beat beat -l info

async def init_crons(sender):
    tags = await service.get_all_tags()
    every_seconds = 10

    sender.add_periodic_task(
        every_seconds,
        tasks.fetch_from_yt_api.s(tags),
    )

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(init_crons(sender))
