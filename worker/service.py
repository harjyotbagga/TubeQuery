import database, utils
from pymongo import UpdateOne, InsertOne, UpdateMany

async def get_all_tags():
    # db_instance = database.get_mongo_client()["TubeQuery"]
    # collection = db_instance["TagList"]
    # try:
    #     tags = []
    #     async for tag in collection.find({"enable": True}):
    #         tags.append(tag)
    #     res_array = utils.MongoObjectToArray(tags)
    #     return res_array
    # except Exception as e:
    #     raise e
    # Sample Tag: 
    # {tag: "tag1", enable: true, description: "tag1 description", frequency: 10}
    return ["cricket", "india", "music", "sports", "tourism", "travel"]


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
        return "Updates Success. upserted_count=%s" % (res.upserted_count,)
    except Exception as e:
        return("add_videos_to_db: exception %s." % (str(e)))
