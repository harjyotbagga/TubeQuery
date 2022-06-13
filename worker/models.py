import datetime

class YT_API_Key:
    def __init__(self, key):
        self.key = key
        self.requests_left = 100
        self.initial_query_time = None
        self.last_query_time = None
    def get_key(self):
        return self.key
    def get_requests_left(self):
        return self.requests_left
    def request_used(self):
        if self.requests_left == 100:
            self.initial_query_time = datetime.datetime.now()
        self.requests_left -= 1
        self.last_query_time = datetime.datetime.now()
    def reset_requests(self):
        self.requests_left = 100
        self.initial_request_time = None
    def is_expired(self):
        if self.requests_left == 0:
            if datetime.timedelta(hours=24) > (datetime.datetime.now() - self.initial_query_time):
                self.reset_requests()
                return False
            else:
                return True
        return False
    def __lt__(self, other):
        return self.requests_left > other.requests_left
