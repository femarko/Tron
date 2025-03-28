from typing import Optional


class AlreadyExistsError(Exception):
    def __init__(self, message_prefix: Optional[str] = ""):
        self.base_message = "with the provided params already existsts."
        self.message = message_prefix + self.base_message


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


class SmthWentWrong(Exception):
    def __init__(self, message: Optional[str] = None):
        self.message = message
