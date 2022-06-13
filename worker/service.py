import database, utils, models
from datetime import datetime
from pymongo import UpdateOne, InsertOne, UpdateMany
from exceptions import NoActiveKeyException, NoTagsException
from models import QUERY_DEDUCTION

async def get_all_tags():
    db_instance = database.get_mongo_client()["TubeQuery"]
    collection = db_instance["Tags"]
    try:
        tag_response = list(collection.find({"enable": True}))
        tags = []
        for tag in tag_response:
            tags.append(tag["tag"])
        return tags
    except Exception as e:
        raise NoTagsException()

def add_videos_to_db(video_items):
    db_instance = database.get_mongo_client()["TubeQuery"]
    video_collection = db_instance["VideoItems"]
    requests = []
    for video_item in video_items:
        video_item_insert = {
            "etag": video_item["etag"],
            "video_id": video_item["id"]["videoId"],
            "channel_id": video_item["snippet"]["channelId"],
            "channel_title": video_item["snippet"]["channelTitle"],
            "published_at": utils.string_to_timestamp(video_item["snippet"]["publishedAt"]),
            "title": video_item["snippet"]["title"],
            "description": video_item["snippet"]["description"],
            "thumbnail_url": video_item["snippet"]["thumbnails"]["default"]["url"],
        }
        requests.append(UpdateOne(
                {'etag': video_item_insert["etag"], 'video_id': video_item_insert["video_id"], 'channel_id': video_item_insert["channel_id"]},
                {"$set": video_item_insert}, upsert=True
            )
        )
    if not requests:
        return "No records upserted as no new video items."
    try:
        res = video_collection.bulk_write(requests)
        return "Updates Success. upserted_count=%s" % (res.upserted_count)
    except Exception as e:
        return("add_videos_to_db: exception %s." % (str(e)))


def get_active_api_key():
    db_instance = database.get_mongo_client()["TubeQuery"]
    collection = db_instance["APIKeys"]
    try:
        APIKey = collection.find_one({}, sort=[("requests_left", -1)])
        print(APIKey)
        if not APIKey:
            raise NoActiveKeyException()
        key = APIKey["key"]
        use_api_key(key)
        return key
    except Exception as e:
        raise e

def use_api_key(key: str):
    db_instance = database.get_mongo_client()["TubeQuery"]
    collection = db_instance["APIKeys"]
    try:
        collection.update_one(
            {"key": key}, 
            {
                "$inc": {"requests_left": -QUERY_DEDUCTION}, 
                "$set": {"last_used_timestamp": datetime.now()}
            }
        )
    except Exception as e:
        raise e