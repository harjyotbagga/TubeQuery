from datetime import datetime

TIMESTAMP_ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def timestamp_to_string(timestamp):
    return timestamp.strftime(TIMESTAMP_ISO_FORMAT)


def string_to_timestamp(string):
    return datetime.strptime(string, TIMESTAMP_ISO_FORMAT)
