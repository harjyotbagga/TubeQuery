class NoActiveKeyException(Exception):
    def __init__(self) -> None:
        self.message = ("No Active API Key is available. Please add new keys to continue.")
        super().__init__(self.message)

class NoTagsException(Exception):
    def __init__(self) -> None:
        self.message = ("No Tags have been added or enabled. Please add new keys to continue.")
        super().__init__(self.message)