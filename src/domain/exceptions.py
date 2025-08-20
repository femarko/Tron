from typing import Optional
from enum import Enum


class DomainExcCodes(str, Enum):
    ALREADY_EXISTS = "ALREADY_EXISTS"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BAD_REQUEST"


class DomainError(Exception): ...


class AlreadyExistsError(DomainError):
    def __init__(
            self,
            message: Optional[str] = None,
            code: DomainExcCodes = DomainExcCodes.ALREADY_EXISTS
    ) -> None:
        self.message = message
        self.code = code


class NotFoundError(DomainError):
    def __init__(
            self,
            message: Optional[str] = None,
            code: DomainExcCodes = DomainExcCodes.NOT_FOUND
    ) -> None:
        self.message = message
        self.code = code


class BadRequestError(DomainError):
    def __init__(
            self,
            message: Optional[str] = None,
            code: DomainExcCodes = DomainExcCodes.BAD_REQUEST
    ) -> None:
        self.message = message
        self.code = code


class UnexpectedParams(DomainError):
    def __init__(
            self,
            message: Optional[str] = None,
            code: str = "UNEXPECTED_PARAMS"
    ):
        self.message = message
        self.code = code

