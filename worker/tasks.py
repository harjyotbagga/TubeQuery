import logging
import requests
import datetime
from celery_app import app
import service

logger = logging.getLogger("tube_beat")
logger.setLevel(logging.INFO)

# Called via dynamic function call, from celery beat
@app.task(name="fetch_from_yt_api")
def fetch_from_yt_api(tags, pageToken=None):
    try:
        key = service.get_active_api_key()
    except Exception as e:
        logger.error("fetch_from_yt_api: ERROR: " + str(e))
        # TODO: Move to Fail Safe Queue
        return

    url = "https://youtube.googleapis.com/youtube/v3/search"
    publishAfterTime = datetime.datetime.now()
    publishBeforeTime = publishAfterTime + datetime.timedelta(seconds=10)
    # DEV: Remove later
    publishAfterTime = datetime.datetime(2022, 6, 14, 0, 0, 0)
    publishBeforeTime = datetime.datetime.now()

    querystring = {
        "part": "snippet",
        "maxResults": "50",
        "order": "date",
        "publishedAfter": publishAfterTime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "publishedBefore": publishBeforeTime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "q": "|".join(tags),
        "type": "video",
        "key": key,
    }
    if pageToken is not None:
        querystring["pageToken"] = pageToken

    response = requests.request("GET", url, params=querystring)
    if response.status_code != 200:
        logger.error("Error: " + str(response.status_code))
        # TODO: Move to Fail Safe Queue
        return

    resp = response.json()
    if resp.get("pageInfo", {}).get("totalResults") == 0:
        return
    if resp.get("nextPageToken") is not None:
        fetch_from_yt_api.delay(tags, resp.get("nextPageToken"))
    video_items = resp.get("items")
    app.send_task("write_to_db", args=[video_items], queue="tube_crud_celery")


# Called via dynamic function call, from celery beat
@app.task(name="write_to_db")
def write_to_db(video_items):
    try:
        msg = service.add_videos_to_db(video_items)
        logger.info(msg)
    except Exception as e:
        logger.error("write_to_db: ERROR: " + str(e))
        # TODO: Move to Fail Safe Queue
    return
