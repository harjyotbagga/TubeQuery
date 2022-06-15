from fastapi import HTTPException


def ResponseModel(data, metadata):
    return {
        "data": data,
        "metadata": metadata,
    }


def ErrorResponseModel(message):
    raise HTTPException(status_code=400, detail=message)
