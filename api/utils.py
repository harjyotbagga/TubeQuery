import datetime
from exceptions import InvalidTimestampException
import time

TIMESTAMP_ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def timestamp_to_string(timestamp):
    try:
        return timestamp.strftime(TIMESTAMP_ISO_FORMAT)
    except Exception as e:
        raise InvalidTimestampException(TIMESTAMP_ISO_FORMAT)


def string_to_timestamp(string):
    try:
        return datetime.datetime.strptime(string, TIMESTAMP_ISO_FORMAT)
    except Exception as e:
        raise InvalidTimestampException(TIMESTAMP_ISO_FORMAT)


def MongoObjectToArray(mobject):
    res = []
    for i in mobject:
        res.append(i)
    return res


def RemoveObjectIdFromMongoObjectArray(mobject):
    res = []
    for i in mobject:
        i.pop("_id")
        res.append(i)
    return res


def stringify_datetime_in_obj(obj):
    if type(obj) is list:
        return [stringify_datetime_in_obj(i) for i in obj]
    if type(obj) is dict:
        return {k: stringify_datetime_in_obj(v) for k, v in obj.items()}
    if type(obj) is datetime.datetime:
        return obj.strftime(TIMESTAMP_ISO_FORMAT)
    return obj
