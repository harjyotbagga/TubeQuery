import heapq as hq
from models import YT_API_Key
import datetime
import time

Active_API_Keys = []
TIMESTAMP_ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

def load_api_keys():
    global Active_API_Keys
    with open('api_keys.txt', 'r') as f:
        keys = f.read().splitlines()
        for key in keys:
            api_key = YT_API_Key(key)
            Active_API_Keys.append(api_key)
    hq.heapify(Active_API_Keys)

def get_active_api_key():
    global Active_API_Keys
    if len(Active_API_Keys) == 0:
        load_api_keys()
    key = hq.heappop(Active_API_Keys)
    if key.is_expired():
        return None
    key.request_used()
    hq.heapify(Active_API_Keys)
    return key.get_key()


def timestamp_to_string(timestamp):
    return timestamp.strftime(TIMESTAMP_ISO_FORMAT)

def string_to_timestamp(string):
    return datetime.datetime.strptime(string, TIMESTAMP_ISO_FORMAT)