from importlib.metadata import metadata
from pydantic import BaseModel
from typing import Union
from datetime import datetime


##############################
# Response Models
##############################
class StandardResponseModel(BaseModel):
    metadata: dict
    data: Union[dict, list, str, None]


##############################
# Request Param Models
##############################
class SearchVideosParams(BaseModel):
    channel_name: Union[str, None] = None
    title: Union[str, None] = None
    description: Union[str, None] = None
    published_before: Union[str, None] = None
    published_after: Union[str, None] = None
    page: Union[int, None] = None
    per_page: Union[int, None] = None

class APIKey(BaseModel):
    key: str
    daily_quota: int
    requests_left: Union[int, None] = None
    created_timestamp: Union[datetime, None] = None
    first_used_timestamp: Union[datetime, None] = None
    last_used_timestamp: Union[datetime, None] = None
