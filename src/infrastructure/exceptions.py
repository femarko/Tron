from typing import Optional
from enum import Enum


class InfrastructureExcCodes(str, Enum):
    REPO_ERROR = "REPO_ERROR"
    DB_ERROR = "DB_ERROR"
    TRON_ERROR = "TRON_ERROR"


class InfrastructureError(Exception): ...


class RepoError(InfrastructureError):
    def __init__(
            self,
            message: Optional[str],
            code: InfrastructureExcCodes = InfrastructureExcCodes.REPO_ERROR
    ) -> None:
        self.message = message
        self.code = code


class DBError(InfrastructureError):
    def __init__(
            self,
            message: Optional[str],
            code: InfrastructureExcCodes = InfrastructureExcCodes.DB_ERROR
    ) -> None:
        self.message = message
        self.code = code


