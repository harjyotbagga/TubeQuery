import logging
from worker import worker
import service
import asyncio
import datetime
import requests


logger = logging.getLogger("failed_tasks")
logger.setLevel(logging.INFO)


# Called via dynamic function call, from celery beat
@worker.task(name="handle_failed_tasks")
def handle_failed_tasks(task_id: int):
    try:
        failed_task = service.get_failed_task(task_id)
        if not failed_task:
            logger.info(f"No failed task found for task_id: {task_id}")
            return
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(failed_requests_handler(task_id, failed_task))

    except Exception as e:
        logger.error(f"handle_failed_tasks: ERROR: {e}")


async def failed_requests_handler(task_id, failed_task):
    task_name = failed_task.get("task_name")
    task_type = failed_task.get("error_type")

    try:
        successful = False
        if task_name == "fetch_from_yt_api":
            if task_type == "No Active API Key" or task_type == "API Keys Exhausted":
                querystring = failed_task.get("request_metdata", {})
                if querystring:
                    successful = fetch_from_yt_api(querystring)
            elif task_type == "Could not get tags":
                tags = service.get_all_tags()
                publishBeforeTime = failed_task.get("timestamp")
                publishAfterTime = publishBeforeTime + datetime.timedelta(
                    seconds=-(2 * 10)
                )
                querystring = {
                    "part": "snippet",
                    "maxResults": "50",
                    "order": "date",
                    "publishedAfter": publishAfterTime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "publishedBefore": publishBeforeTime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "q": "|".join(tags),
                    "type": "video",
                }
                successful = fetch_from_yt_api(querystring)
        elif failed_task.get("task_name") == "write_to_db":
            video_items = failed_task.get("request_metadata", {}).get("videos", [])
            successful = write_to_db(video_items)
        else:
            logger.info(
                f"No handler found for task_name: {failed_task.get('task_name')}"
            )
    except Exception:
        successful = False

    if not successful:
        logger.info(f"Task {task_id} failed yet again.")
    else:
        logger.info(f"Task {task_id} succeeded.")
    service.update_task_status(task_id, successful)


def fetch_from_yt_api(querystring, pageToken=None):
    try:
        key = service.get_active_api_key()
    except Exception as e:
        logger.error("fetch_from_yt_api: ERROR: " + str(e))
        return False

    url = "https://youtube.googleapis.com/youtube/v3/search"

    if pageToken is not None:
        querystring["pageToken"] = pageToken

    response = requests.request("GET", url, params=querystring)
    if response.status_code != 200:
        logger.info(f"fetch_from_yt_api: ERROR: {response.status_code}")
        return False

    resp = response.json()
    if resp.get("pageInfo", {}).get("totalResults") == 0:
        logger.info("fetch_from_yt_api: 0 videos found")
        return True

    video_items = resp.get("items")
    logger.info("fetch_from_yt_api: " + str(len(video_items)) + " videos found")
    return write_to_db(video_items)


def write_to_db(video_items):
    try:
        msg = service.add_videos_to_db(video_items)
        logger.info(msg)
        return True
    except Exception as e:
        logger.error("write_to_db: ERROR: " + str(e))
    return False
