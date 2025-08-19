from typing import Optional

from src.application.exceptions import ApplicationError, AppExcCodes
from src.domain.exceptions import DomainError, DomainExcCodes


class ValidationError(DomainError):
    def __init__(
            self,
            message: Optional[str] = None,
            code: DomainExcCodes = DomainExcCodes.VALIDATION_ERROR
    ) -> None:
        self.message = message
        self.code = code


class ConfigError(ApplicationError):
    def __init__(
            self,
            message: Optional[str],
            code: AppExcCodes = AppExcCodes.INTERNAL_SERVER_ERROR
    ) -> None:
        self.message = message
        self.code = code
