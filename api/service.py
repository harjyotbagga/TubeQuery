from datetime import datetime
from schemas import *
from database import *
from utils import *

DATABASE_NAME = os.getenv("DB_NAME", "TubeQuery")


def query_videos(filters: dict, optionals: dict = {}):
    db_instance = get_mongo_client()[DATABASE_NAME]
    collection = db_instance["VideoItems"]
    try:
        match_filters = filters
        skip = optionals.get("skip", 0)
        limit = optionals.get("limit", 10)
        page = optionals.get("page", 1)
        text_tags = match_filters.pop("tags", None)
        project = {
            "_id": 0,
            "title": 1,
            "description": 1,
            "published_at": 1,
            "channel_title": 1,
            "thumbnail_url": 1,
        }
        pipeline = []

        if text_tags:
            match_filters["$text"] = {"$search": text_tags}
        if match_filters:
            pipeline.append({"$match": match_filters})

        pipeline += [
            {"$project": project},
            {"$sort": {"published_at": -1}},
        ]
        pipeline.append({"$skip": skip})
        pipeline.append(
            {"$facet": {"data": [{"$limit": limit}], "total": [{"$count": "count"}]}}
        )
        pipeline_result = list(collection.aggregate(pipeline))
        result = pipeline_result[0]["data"]
        if len(result) == 0:
            total_counts = 0
        else:
            total_counts = pipeline_result[0]["total"][0]["count"] + skip

        if (page * limit) >= total_counts:
            next_page = None
        else:
            next_page = page + 1
        metadata = {
            "total_counts": total_counts,
            "result_counts": len(result),
            "next_page": next_page,
            "limit": limit,
        }
        return result, metadata
    except Exception as e:
        raise e


def get_api_keys(filters: dict, optionals: dict = {}):
    db_instance = get_mongo_client()[DATABASE_NAME]
    collection = db_instance["APIKeys"]
    try:
        skip = optionals.get("skip", 0)
        limit = optionals.get("limit", 10)
        page = optionals.get("page", 1)
        project = {
            "_id": 0,
        }
        pipeline = []
        if filters:
            pipeline.append({"$match": filters})
        pipeline += [
            {"$project": project},
            {"$sort": {"created_at": -1}},
        ]
        pipeline.append({"$skip": skip})
        pipeline.append(
            {"$facet": {"data": [{"$limit": limit}], "total": [{"$count": "count"}]}}
        )
        pipeline_result = list(collection.aggregate(pipeline))
        result = pipeline_result[0]["data"]

        if len(result) == 0:
            total_counts = 0
        else:
            total_counts = pipeline_result[0]["total"][0]["count"] + skip

        if (page * limit) >= total_counts:
            next_page = None
        else:
            next_page = page + 1
        metadata = {
            "total_counts": total_counts,
            "result_counts": len(result),
            "next_page": next_page,
            "limit": limit,
        }
        return result, metadata
    except Exception as e:
        raise e


def create_api_key(NewAPIKey: APIKey):
    db_instance = get_mongo_client()[DATABASE_NAME]
    collection = db_instance["APIKeys"]
    try:
        NewAPIKey.created_at = datetime.datetime.now()
        NewAPIKey.requests_left = NewAPIKey.daily_quota
        collection.update_one(
            {"key": NewAPIKey.key}, {"$setOnInsert": NewAPIKey.dict()}, upsert=True
        )
        return NewAPIKey
    except Exception as e:
        raise e


def get_tags(filters: dict, optionals: dict = {}):
    db_instance = get_mongo_client()[DATABASE_NAME]
    collection = db_instance["Tags"]
    try:
        skip = optionals.get("skip", 0)
        limit = optionals.get("limit", 10)
        page = optionals.get("page", 1)
        project = {
            "_id": 0,
        }
        pipeline = []
        if filters:
            pipeline.append({"$match": filters})
        pipeline += [
            {"$project": project},
            {"$sort": {"created_at": -1}},
        ]
        pipeline.append({"$skip": skip})
        pipeline.append(
            {"$facet": {"data": [{"$limit": limit}], "total": [{"$count": "count"}]}}
        )
        pipeline_result = list(collection.aggregate(pipeline))
        result = pipeline_result[0]["data"]

        if len(result) == 0:
            total_counts = 0
        else:
            total_counts = pipeline_result[0]["total"][0]["count"] + skip

        if (page * limit) >= total_counts:
            next_page = None
        else:
            next_page = page + 1
        metadata = {
            "total_counts": total_counts,
            "result_counts": len(result),
            "next_page": next_page,
            "limit": limit,
        }
        return result, metadata
    except Exception as e:
        raise e


def create_tag(NewTag: Tag):
    db_instance = get_mongo_client()[DATABASE_NAME]
    collection = db_instance["Tags"]
    try:
        NewTag.created_at = datetime.datetime.now()
        collection.update_one({"tag": NewTag.tag}, {"$set": NewTag.dict()}, upsert=True)
        return NewTag
    except Exception as e:
        raise e
