from fastapi.responses import JSONResponse

from src.application.exceptions import (
    AppExcCodes,
    ApplicationError
)
from src.interfaces.fastapi_app.schemas import FailedRequest

exception_code_to_http_code = {
    AppExcCodes.BUISINESS_RULE_VIOLATION: 400,
    AppExcCodes.INTERNAL_SERVER_ERROR: 500,
    AppExcCodes.STORAGE_ERROR: 500,
    AppExcCodes.EXTERNAL_SERVICE_ERROR: 500,
    AppExcCodes.UNIQUE_CONSTRAINT_VIOLATION: 400,
    AppExcCodes.NOT_FOUND: 404,
    AppExcCodes.BAD_REQUEST: 400
}

def app_exception_handler(exc: ApplicationError, **kwargs) -> JSONResponse:
    return JSONResponse(
        status_code=exception_code_to_http_code[exc.code],
        content=FailedRequest(address=kwargs.get("address"), error=exc.message).model_dump()
    )
