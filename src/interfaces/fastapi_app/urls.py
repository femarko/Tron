from fastapi import APIRouter
from decimal import Decimal
from typing import cast

from src.interfaces.fastapi_app.schemas import Addr
from src.application import app_manager, unit_of_work
from src.infrastructure.orm.sql_aclchemy_wrapper import orm_conf
from src.bootstrap.bootstrap import container



tron_router = APIRouter()


# @tron_router.post("/address_info")
# def get_address_info(addr: Addr,) -> dict[str, int | Decimal]:
#     addr_info: dict[str, int | Decimal] = {
#         "balance": app_manager.get_balance(addr=addr.addr),
#         "energy": app_manager.get_energy_and_bandwidth(addr=addr.addr).get("energy"),
#         "bandwidth": app_manager.get_energy_and_bandwidth(addr=addr.addr).get("bandwidth")
#     }
#     id = app_manager.save_address_info(
#         data=cast(dict, {"address": addr.addr, **addr_info}),
#         uow=unit_of_work.UnitOfWork(session_maker=orm_conf.session_maker)
#     )
#
#     return {"id": id, **addr_info}

@tron_router.post("/address_info")
def get_address_info(addr: Addr,) -> dict[str, int | Decimal]:
    addr_info: dict[str, int | Decimal] = container.load_address_info_from_tron_use_case.execute(addr=addr)
    return addr_info

# @tron_router.get("/get_info_from_db")
# def get_info_from_db(number: int = 20,
#                      page: int = 1,
#                      per_page: int = 5) -> dict[str, int | list[dict[str, str |int | Decimal]]]:
#     return app_manager.get_info_from_db(
#         number=number, page=page, per_page=per_page, uow=unit_of_work.UnitOfWork(session_maker=orm_conf.session_maker)
#     )

@tron_router.get("/get_info_from_db")
def get_info_from_db(number: int = 20,
                     page: int = 1,
                     per_page: int = 5) -> dict[str, int | list[dict[str, str |int | Decimal]]]:
    return container.retrieve_address_info_from_db_use_case.execute(
        number=number,
        page=page,
        per_page=per_page,
        uow=container.uow
    )
