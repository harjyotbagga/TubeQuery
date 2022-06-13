from datetime import datetime
from schemas import *
from database import *
from utils import timestamp_to_string, string_to_timestamp
from utils import *

def query_videos(filters: dict, optionals: dict = {}):
    db_instance = get_mongo_client()["TubeQuery"]
    video_collection = db_instance["VideoItems"]
    try:
        total_counts = video_collection.count_documents(filters)
        project = {
            "title": 1,
            "description": 1,
            "published_at": 1,
            "channel_title": 1,
            "thumbnail_url": 1,
        }
        video_items = video_collection.find(filters, project).sort("published_at", -1).limit(optionals.get("limit", 10)).skip(optionals.get("skip", 0))
        video_items = RemoveObjectIdFromMongoObjectArray(video_items)
        if (optionals.get("page", 1) * optionals.get("limit", 10)) >= total_counts:
            next_page = None
        else:
            next_page = optionals.get("page", 1) + 1
        metadata = {
            "total_counts": total_counts,
            "result_counts": len(video_items),
            "next_page": next_page,
            "limit": optionals.get("limit", 10),
        }
        
        return video_items, metadata
    except Exception as e:
        raise e
    