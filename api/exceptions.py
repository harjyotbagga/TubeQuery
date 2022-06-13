class InvalidTimestampException(Exception):
    def __init__(self, valid_timestamp) -> None:
        self.message = (f"Please pass the timestamp in ${valid_timestamp} format")
        super().__init__(self.message)