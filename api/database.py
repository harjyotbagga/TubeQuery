import os
import logging
from pymongo import MongoClient

logger = logging.getLogger("database")

MONGO_DB_LINK = os.getenv("MONGO_DB_LINK", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DB_NAME", "TubeQuery")

DB_CONNECTION = None

def get_mongo_client():
    global DB_CONNECTION, DATABASE_NAME
    if DB_CONNECTION is None:
        DB_CONNECTION = MongoClient(MONGO_DB_LINK, connect=False)
    return DB_CONNECTION