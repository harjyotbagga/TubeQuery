from fastapi import FastAPI, Request, Depends
from response import *
from service import *
from typing import Union

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
    page: Union[int, None] = None,
    per_page: Union[int, None] = None,
    ):
    try:
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
            q["title"] = title
        if description:
            q["description"] = description
        print(q)
        response_arr = query_videos(q)
        return ResponseModel(response_arr, {})
    except Exception as e:
        return ErrorResponseModel(str(e))
