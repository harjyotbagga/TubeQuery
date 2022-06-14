import datetime
import pytz

DAILY_QUOTA = 10000
QUERY_DEDUCTION = 100


class YT_API_Key:
    def __init__(
        self, key, created_at, daily_quota, last_used_timestamp, requests_left
    ):
        self.key = key
        self.created_at = created_at
        self.daily_quota = daily_quota
        self.last_used_timestamp = last_used_timestamp
        self.requests_left = requests_left

    def get_key(self):
        return self.key

    def get_requests_left(self):
        return self.requests_left

    def reset_requests(self):
        self.requests_left = self.daily_quota

    def daily_reset(self):
        last_used_timestamp_pacific = self.last_used_timestamp.astimezone(
            pytz.timezone("US/Pacific")
        )
        today_pacific = datetime.datetime.now().astimezone(pytz.timezone("US/Pacific"))
        today_pacific_start = datetime.datetime(
            today_pacific.year,
            today_pacific.month,
            today_pacific.day,
            0,
            0,
            0,
            0,
            pytz.timezone("US/Pacific"),
        )
        if last_used_timestamp_pacific < today_pacific_start:
            self.reset_requests()

    def request_used(self):
        if self.daily_reset:
            self.reset_requests()
        self.requests_left -= QUERY_DEDUCTION
        self.last_used_timestamp = datetime.datetime.now()

    def is_expired(self):
        if self.requests_left <= 0:
            if self.daily_reset:
                self.reset_requests()
                return False
            else:
                return True
        return False

    def __lt__(self, other):
        return self.requests_left > other.requests_left
