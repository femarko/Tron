from fastapi import APIRouter
from decimal import Decimal

from src.interfaces.fastapi_app.schemas import Addr
from src.bootstrap.bootstrap import container


tron_router = APIRouter()


@tron_router.post("/address_info")
def get_address_info(addr: Addr,) -> dict[str, str | int | Decimal]:
    addr_info: dict[str, int | Decimal] = container.load_address_info_from_tron_use_case.execute(addr=addr.addr)
    return addr_info


@tron_router.get("/get_info_from_db")
def get_info_from_db(number: int = 20,
                     page: int = 1,
                     per_page: int = 5) -> dict[str, int | list[dict[str, str |int | Decimal]]]:
    return container.retrieve_address_info_from_db_use_case.execute(
        number=number,
        page=page,
        per_page=per_page
    )
