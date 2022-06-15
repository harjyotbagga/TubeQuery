import datetime
from pydantic import BaseModel
from typing import Optional


class FailedTask(BaseModel):
    task_id: str

    class Config:
        orm_mode = True
