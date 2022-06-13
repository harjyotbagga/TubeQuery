from datetime import datetime
from schemas import *
from ops import *
from utils import timestamp_to_string, string_to_timestamp
from utils import *

def query_videos(filters: dict):
    db_instance = database.get_mongo_client()["TubeQuery"]
    video_collection = db_instance["VideoItems"]
    try:
        video_items = video_collection.find(filters).sort("published_at", -1)
        video_items = RemoveObjectIdFromMongoObjectArray(video_items)
        # print(video_items)
        return video_items
    except Exception as e:
        raise e
    