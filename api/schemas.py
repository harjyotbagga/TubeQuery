from pydantic import BaseModel
from typing import Union
from datetime import datetime

class APIKey(BaseModel):
    key: str
    daily_quota: int
    requests_left: Union[int, None] = None
    created_at: Union[datetime, None] = None
    last_used_timestamp: Union[datetime, None] = None

class Tag(BaseModel):
    tag: str
    enable: bool = True
    created_at: Union[datetime, None] = None
