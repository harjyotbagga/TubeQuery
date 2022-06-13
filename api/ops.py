import database

def get_video_from_db(filters: dict):
    db_instance = database.get_mongo_client()["TubeQuery"]
    video_collection = db_instance["VideoItems"]
    try:
        video_items = video_collection.find(filters, {"published_at": -1})
        return video_items
    except Exception as e:
        raise e