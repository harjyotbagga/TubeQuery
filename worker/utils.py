import heapq as hq
from models import YT_API_Key
from database import get_mongo_client
from service import get_active_api_key, use_api_key
import datetime
import time

TIMESTAMP_ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

def timestamp_to_string(timestamp):
    return timestamp.strftime(TIMESTAMP_ISO_FORMAT)

def string_to_timestamp(string):
    return datetime.datetime.strptime(string, TIMESTAMP_ISO_FORMAT)