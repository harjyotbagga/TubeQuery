from fastapi import FastAPI, Header
from response import *
import tasks, schemas
import logging
import subprocess

logger = logging.getLogger("failed_task_api")
logger.setLevel(logging.INFO)

app = FastAPI()


@app.get("/")
async def root():
    return ResponseModel(data="Hello World!", metadata={"success": True})


@app.post("/tasks")
async def get_tasks(payload: schemas.FailedTask):
    try:
        tasks.handle_failed_tasks.delay(payload.task_id)
        return ResponseModel(data="Task queued", metadata={"success": True})
    except Exception as e:
        logger.error(e)
        return ErrorResponseModel(str(e))
