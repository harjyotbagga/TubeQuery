from importlib.metadata import metadata
from pydantic import BaseModel
from typing import Union


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