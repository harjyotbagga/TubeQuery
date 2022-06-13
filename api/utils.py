import datetime
import time

TIMESTAMP_ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

def timestamp_to_string(timestamp):
    try:
        return timestamp.strftime(TIMESTAMP_ISO_FORMAT)
    except Exception as e:
        raise e

def string_to_timestamp(string):
    try:
        return datetime.datetime.strptime(string, TIMESTAMP_ISO_FORMAT)
    except Exception as e:
        raise e

def MongoObjectToArray(mobject):
    res = []
    for i in mobject:
        res.append(i)
    return res

def RemoveObjectIdFromMongoObjectArray(mobject):
    res = []
    for i in mobject:
        i.pop('_id')
        res.append(i)
    return res