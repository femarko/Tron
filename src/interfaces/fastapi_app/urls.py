from fastapi import APIRouter
from fastapi.responses import JSONResponse
from decimal import Decimal

from src.interfaces.fastapi_app.schemas import (
    Addr,
    FailedRequestToTron
)
from src.bootstrap.bootstrap import container
from src.interfaces.fastapi_app.schemas import (
    AddressInfoFromTron,
    EntriesFromDB,
)
from src.application.exceptions import ApplicationError
from src.interfaces.fastapi_app.exceptions import app_exception_handler


tron_router = APIRouter()


@tron_router.post(
    path="/address_info_from_tron",
    response_model=AddressInfoFromTron,
    tags=["address_info"],
    summary="Get address info from TRON network",
    description="Obtain balance, energy, and bandwidth from the TRON network "
                "for a specific address that is specified in the POST request payload.",
    status_code=201,
    responses={
        201: {
            "model": AddressInfoFromTron,
            "description": "Address info successfully obtained from the TRON network and respective entry saved in DB."
        },
        400: {
            "model": FailedRequestToTron,
            "description": "Bad request."
        },
        404: {
            "model": FailedRequestToTron,
            "description": "Address not found."
        },
        500: {
            "model": FailedRequestToTron,
            "description": "Internal server error."
        }
    }
)
def get_address_info(addr: Addr) -> AddressInfoFromTron | JSONResponse:
    try:
        addr_info: dict[str, int | Decimal] = container.load_address_info_from_tron_use_case.execute(addr=addr.addr)
        return AddressInfoFromTron(**addr_info)
    except ApplicationError as e:
        return app_exception_handler(exc=e, address=addr.addr)


@tron_router.get(
    path="/recent_records",
    response_model=EntriesFromDB,

)
def get_info_from_db(
        number: int = 20,
        page: int = 1,
        per_page: int = 5
) -> EntriesFromDB | JSONResponse:
    try:
        return container.retrieve_address_info_from_db_use_case.execute(
            number=number,
            page=page,
            per_page=per_page
        )
    except ApplicationError as e:
        print(f"From urls.get_info_from_db - Exception: {e = }, {str(e.message) = }")  # todo: remove
        return app_exception_handler(exc=e)
