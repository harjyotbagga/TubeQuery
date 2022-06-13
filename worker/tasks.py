import requests
import datetime
from celery_app import app
import service

# TODO: Enable Logging

# Called via dynamic function call, from celery beat
@app.task(name="fetch_from_yt_api")
def fetch_from_yt_api(tags, pageToken=None):
    try:
        key = service.get_active_api_key()
    except Exception as e:
        print("fetch_from_yt_api: ERROR: " + str(e))
        return

    url = "https://youtube.googleapis.com/youtube/v3/search"
    publishAfterTime = datetime.datetime.now()
    publishBeforeTime = publishAfterTime + datetime.timedelta(seconds=10)
    
    querystring = {
        "part":"snippet",
        "maxResults":"50",
        "order":"date",
        "publishedAfter":publishAfterTime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "publishedBefore":publishBeforeTime.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "q":"|".join(tags),
        "type":"video",
        "key":key
    }
    if pageToken is not None:
        querystring["pageToken"] = pageToken

    response = requests.request("GET", url, params=querystring)
    if response.status_code != 200:
        print("Error: " + str(response.status_code))
        return
    
    resp = response.json()
    if resp.get('pageInfo', {}).get('totalResults') == 0:
        print("No results found")
        return
    if resp.get('nextPageToken') is not None:
        fetch_from_yt_api.delay(tags, resp.get('nextPageToken'))
    video_items = resp.get('items')
    write_to_db.delay(video_items)


# Called via dynamic function call, from celery beat
@app.task(name="write_to_db")
def write_to_db(video_items):
    try:
        msg = service.add_videos_to_db(video_items)
        # logger.info("pull_vendor_permit_data: create_permits for site_id=%s, vendor_name=%s, from_ts=%s, to_ts=%s" % (site_id, vendor_name, from_ts, to_ts))
    except Exception as e:
        err = str(e)
        # response_time_seconds = (datetime.datetime.utcnow() - start_time).total_seconds()
        # service.add_vendor_api_logs(service.SOURCE_INSERT, service.PermitData, site_id, vendor_name, implementation_type, len(permits), response_time_seconds, err)
        raise e

    return msg