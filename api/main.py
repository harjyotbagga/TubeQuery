from fastapi import FastAPI, Request, Depends
from cache import *
from response import *
from service import *
from database import setup_db, load_api_keys
from typing import Union
from schemas import APIKey
from utils import stringify_datetime_in_obj
import logging
import os
import json

logger = logging.getLogger("tube_api")
logger.setLevel(logging.INFO)

app = FastAPI()

setup_db()
client = redis_connect()

LOAD_API_KEYS = os.getenv("LOAD_API_KEYS", False)
if LOAD_API_KEYS:
    load_api_keys()


@app.get("/")
async def root():
    return ResponseModel(data="Hello World!", metadata={"success": True})


@app.get("/video/search")
async def search_videos(
    request: Request,
    title: Union[str, None] = None,
    description: Union[str, None] = None,
    published_before: Union[str, None] = None,
    published_after: Union[str, None] = None,
    channel_title: Union[str, None] = None,
    tags: Union[str, None] = None,
    page: Union[int, None] = 1,
    limit: Union[int, None] = 10,
):
    try:
        skips = (page - 1) * limit
        optionals = {
            "limit": limit,
            "skip": skips,
            "page": page,
        }
        q = {}
        pushlish_query = {}
        if published_before:
            published_before = string_to_timestamp(published_before)
            pushlish_query["$lte"] = published_before
        if published_after:
            published_after = string_to_timestamp(published_after)
            pushlish_query["$gte"] = published_after
        if pushlish_query:
            q["published_at"] = pushlish_query
        if channel_title:
            q["channel_title"] = channel_title
        if title:
            q["title"] = {"$regex": title, "$options": "i"}
        if description:
            q["description"] = {"$regex": description, "$options": "i"}
        if tags:
            q["tags"] = tags
        response_arr, metadata = query_videos(q, optionals)
        return ResponseModel(response_arr, metadata)
    except Exception as e:
        logger.error(e)
        return ErrorResponseModel(str(e))


@app.get("/video/search/tags")
async def search_videos_by_tags(
    request: Request,
    tags: Union[str, None] = None,
    page: Union[int, None] = 1,
    limit: Union[int, None] = 10,
):
    try:
        skips = (page - 1) * limit
        optionals = {
            "limit": limit,
            "skip": skips,
            "page": page,
        }
        q = {}
        if tags:
            q["tags"] = tags
        data = get_tag_results_from_cache(tags)
        if data is not None:
            data_metadata = get_tag_results_from_cache(f"${tags}_metadata")
            if data_metadata is not None:
                return ResponseModel(json.loads(data), json.loads(data_metadata))
        response_arr, metadata = query_videos(q, optionals)
        set_tag_results_to_cache(
            tags, json.dumps(stringify_datetime_in_obj(response_arr))
        )
        set_tag_results_to_cache(f"${tags}_metadata", json.dumps(metadata))
        return ResponseModel(response_arr, metadata)
    except Exception as e:
        logger.error(e)
        return ErrorResponseModel(str(e))


@app.get("/keys")
async def search_api_keys(
    request: Request,
    key: str = None,
    limit: Union[int, None] = 10,
    page: Union[int, None] = 1,
):
    try:
        skips = (page - 1) * limit
        optionals = {
            "limit": limit,
            "skip": skips,
            "page": page,
        }
        q = {}
        if key:
            q["key"] = key
        response_arr, metadata = get_api_keys(q, optionals)
        return ResponseModel(response_arr, metadata)
    except Exception as e:
        logger.error(e)
        return ErrorResponseModel(str(e))


@app.post("/keys")
async def add_api_keys(
    request: Request,
    NewAPIKey: APIKey,
):
    try:
        key = create_api_key(NewAPIKey)
        return ResponseModel(key, {"success": True})
    except Exception as e:
        logger.error(e)
        return ErrorResponseModel(str(e))


@app.get("/tags")
async def search_tags(
    request: Request,
    tag: str = None,
    limit: Union[int, None] = 10,
    page: Union[int, None] = 1,
):
    try:
        skips = (page - 1) * limit
        optionals = {
            "limit": limit,
            "skip": skips,
            "page": page,
        }
        q = {}
        if tag:
            q["tag"] = tag
        response_arr, metadata = get_tags(q, optionals)
        return ResponseModel(response_arr, metadata)
    except Exception as e:
        logger.error(e)
        return ErrorResponseModel(str(e))


@app.post("/tags")
async def add_api_keys(
    request: Request,
    NewTag: Tag,
):
    try:
        tag = create_tag(NewTag)
        return ResponseModel(tag, {"success": True})
    except Exception as e:
        logger.error(e)
        return ErrorResponseModel(str(e))
