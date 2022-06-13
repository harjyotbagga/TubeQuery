import heapq as hq
from models import YT_API_Key

Active_API_Keys = []


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