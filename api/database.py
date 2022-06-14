import os
import logging
import pymongo
from datetime import datetime
from schemas import APIKey
from pymongo import MongoClient

logger = logging.getLogger("database")
logger.setLevel(logging.INFO)

MONGO_DB_LINK = os.getenv("MONGO_DB_LINK", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DB_NAME", "TubeQuery")

DB_CONNECTION = None


def setup_db():
    client = get_mongo_client()
    db = client[DATABASE_NAME]
    collections_exist = db.list_collection_names()
    if "APIKeys" not in collections_exist:
        db.create_collection("APIKeys")
        api_collection = db["APIKeys"]
        api_collection.create_index("requests_left", pymongo.DESCENDING)
    if "VideoItems" not in collections_exist:
        db.create_collection("VideoItems")
        video_collection = db["VideoItems"]
        video_collection.create_index(
            [("title", pymongo.TEXT), ("description", pymongo.TEXT)]
        )
    if "Tags" not in collections_exist:
        db.create_collection("Tags")
        tag_collection = db["Tags"]
        tag_collection.create_index("tag")


def load_api_keys():
    try:
        with open("api_keys.txt") as f:
            api_keys = f.read().splitlines()
        db = get_mongo_client()[DATABASE_NAME]
        api_collection = db["APIKeys"]
        requests = []
        for api_key in api_keys:
            key = APIKey(
                key=api_key,
                daily_quota=10000,
                created_at=datetime.now(),
                requests_left=10000,
            )
            requests.append(
                pymongo.UpdateOne(
                    {"key": key.key}, {"$setOnInsert": key.dict()}, upsert=True
                )
            )
        res = api_collection.bulk_write(requests)
        logger.info("%s new API Keys Loaded." % (res.upserted_count))
    except Exception as e:
        logger.error(e)


def get_mongo_client():
    global DB_CONNECTION
    if DB_CONNECTION is None:
        DB_CONNECTION = MongoClient(MONGO_DB_LINK, connect=False)
    return DB_CONNECTION
