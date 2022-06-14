from fastapi import FastAPI, Request, Depends
from pytz import utc
from response import *
from service import *
from typing import Union
from schemas import APIKey
import logging

logger = logging.getLogger("tube_api")
logger.setLevel(logging.INFO)

app = FastAPI()

@app.get("/")
async def root():
    return ResponseModel(data="Hello World!", metadata={"success": True})


@app.get("/video/search")
async def search_videos(request: Request,
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
        q =  {}
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


@app.get("/keys")
async def search_api_keys(request: Request,
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
async def add_api_keys(request: Request,
    NewAPIKey: APIKey,
    ):
    try:
        key = create_api_key(NewAPIKey)
        return ResponseModel(key, {"success": True})
    except Exception as e:
        logger.error(e)
        return ErrorResponseModel(str(e))


@app.get("/tags")
async def search_tags(request: Request,
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
async def add_api_keys(request: Request,
    NewTag: Tag,
    ):
    try:
        tag = create_tag(NewTag)
        return ResponseModel(tag, {"success": True})
    except Exception as e:
        logger.error(e)
        return ErrorResponseModel(str(e))

