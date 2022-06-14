import logging
import requests
import datetime
import json
from celery_app import app
import service
from exceptions import NoTagsException

logger = logging.getLogger("tube_beat")
logger.setLevel(logging.INFO)

# Called via dynamic function call, from celery beat
@app.task(name="fetch_from_yt_api")
def fetch_from_yt_api(pageToken=None):
    try:
        tags = service.get_all_tags()
    except NoTagsException:
        logger.info("No tags added yet, skipping cron initialization")
        return
    except Exception as e:
        service.log_failed_requests(
            "fetch_from_yt_api",
            "Could not get tags",
            str(e),
            datetime.datetime.now(),
            {},
            None,
            None,
        )
        logger.error("fetch_from_yt_api: ERROR: " + str(e))
        return

    try:
        key = service.get_active_api_key()
    except Exception as e:
        logger.error("fetch_from_yt_api: ERROR: " + str(e))
        service.log_failed_requests(
            "fetch_from_yt_api",
            "No Active API Key",
            str(e),
            datetime.datetime.now(),
            {"tags": tags},
            None,
            None,
        )
        return

    url = "https://youtube.googleapis.com/youtube/v3/search"
    publishBeforeTime = datetime.datetime.now()
    publishAfterTime = publishBeforeTime + datetime.timedelta(seconds=-(2 * 10))

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
        logger.error(
            "Error: Non 200 Status Code Response. Response Status Code: "
            + str(response.status_code)
        )
        service.log_failed_requests(
            "fetch_from_yt_api",
            "API Keys Exhausted",
            "Non 200 Status Response",
            datetime.datetime.now(),
            querystring,
            response.status_code,
            response.json(),
        )
        return

    resp = response.json()

    # DEV: Return Sample Response from json file
    # with open("./sample_resp.json") as f:
    #     resp = json.load(f)

    # if resp.get("pageInfo", {}).get("totalResults") == 0:
    #     logger.info("fetch_from_yt_api: 0 videos found")
    #     return

    if resp.get("nextPageToken") is not None:
        fetch_from_yt_api.delay(resp.get("nextPageToken"))
    video_items = resp.get("items")
    logger.info("fetch_from_yt_api: " + str(len(video_items)) + " videos found")
    app.send_task("write_to_db", args=[video_items], queue="tube_crud_celery")


# Called via dynamic function call, from celery beat
@app.task(name="write_to_db")
def write_to_db(video_items):
    try:
        msg = service.add_videos_to_db(video_items)
        logger.info(msg)
    except Exception as e:
        logger.error("write_to_db: ERROR: " + str(e))
        service.log_failed_requests(
            "write_to_db",
            "DB Write Failed",
            str(e),
            datetime.datetime.now(),
            {"video_items": video_items},
            None,
            None,
        )
    return
