from typing import Optional
from enum import Enum

import src.bootstrap.exceptions
import src.infrastructure.tron.exceptions
from src.domain import exceptions as domain_exceptions
from src.infrastructure import exceptions as infrastructure_exceptions


# DOMAIN_EXCEPTIONS = (
#     domain_exceptions.DomainError,
#     domain_exceptions.NotFoundError,
#     src.bootstrap.exceptions.ValidationError,
#     domain_exceptions.AlreadyExistsError
# )
#
# INFRASTRUCTURE_EXCEPTIONS = (
#     infrastructure_exceptions.InfrastructureError,
#     infrastructure_exceptions.RepoError,
#     infrastructure_exceptions.DBError,
#     infrastructure_exceptions.TronError
# )


class AppExcCodes(str, Enum):
    BUISINESS_RULE_VIOLATION = "BUSINESS_RULE_VIOLATION"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    STORAGE_ERROR = "STORAGE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    UNIQUE_CONSTRAINT_VIOLATION = "UNIQUE_CONSTRAINT_VIOLATION"
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BAD_REQUEST"


class ApplicationError(Exception):
    def __init__(
            self,
            message: Optional[str] = "Internal Server Error",
            code: AppExcCodes = AppExcCodes.INTERNAL_SERVER_ERROR
    ) -> None:
        self.message = message
        self.code = code


def app_exception_mapper(exc: Exception) -> ApplicationError:
    if isinstance(exc, (infrastructure_exceptions.RepoError, infrastructure_exceptions.DBError)):
        return ApplicationError(message=exc.message, code=AppExcCodes.STORAGE_ERROR)
    if isinstance(exc, src.infrastructure.tron.exceptions.TronError):
        return ApplicationError(message=exc.message, code=AppExcCodes.EXTERNAL_SERVICE_ERROR)
    if isinstance(exc, domain_exceptions.NotFoundError):
        return ApplicationError(message=exc.message, code=AppExcCodes.NOT_FOUND)
    if isinstance(exc, domain_exceptions.BadRequestError):
        return ApplicationError(message=exc.message, code=AppExcCodes.BAD_REQUEST)
    if isinstance(exc, domain_exceptions.AlreadyExistsError):
        return ApplicationError(message=exc.message, code=AppExcCodes.UNIQUE_CONSTRAINT_VIOLATION)
    return ApplicationError()
