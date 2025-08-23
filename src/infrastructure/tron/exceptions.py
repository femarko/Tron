from typing import Optional

from src.infrastructure.exceptions import InfrastructureError, InfrastructureExcCodes
from src.infrastructure.tron.import_handler import import_as_mapping
from src.domain.exceptions import (
    NotFoundError,
    BadRequestError
)


tron_exceptions: dict[str, type] = import_as_mapping("tronpy.exceptions")
NOT_FOUND_TR_ERRORS = tuple(v for k, v in tron_exceptions.items() if k.endswith("NotFound") or k.startswith("NotFound"))
BAD_DATA_TR_ERRORS = tuple(v for k, v in tron_exceptions.items() if k.endswith("Bad") or k.startswith("Bad"))
OTHER_TR_ERRORS = tuple(v for k, v in tron_exceptions.items() if v not in (*NOT_FOUND_TR_ERRORS, *BAD_DATA_TR_ERRORS))

tron_exceptions_types = {
    "not_found": NOT_FOUND_TR_ERRORS,
    "bad_data": BAD_DATA_TR_ERRORS,
    "other": OTHER_TR_ERRORS
}

class TronError(InfrastructureError):
    def __init__(
            self,
            message: Optional[str],
            code: InfrastructureExcCodes = InfrastructureExcCodes.TRON_ERROR
    ) -> None:
        self.message = message
        self.code = code


def tron_exc_mapper(exc: Exception, exception_types: dict[str, tuple[Exception]]) -> Exception:
    if isinstance(exc, exception_types.get("not_found")):
        return NotFoundError(message=str(exc))
    if isinstance(exc, exception_types.get("bad_data")):
        return BadRequestError(message=f"Wrong input data: {str(exc)}")
    return TronError(message=str(exc))
