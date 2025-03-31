from decimal import Decimal

import fastapi
from fastapi.params import Depends
from typing import cast

from src.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.service_layer import app_manager, unit_of_work
from pydantic import BaseModel


app = fastapi.FastAPI(dependencies=[Depends(orm_conf.start_mapping)])


class Addr(BaseModel):
    addr: str


@app.post("/address_info")
def get_address_info(
        addr: Addr,#str = fastapi.Body(..., embed=True),
) -> dict[str, int | Decimal]:
    addr_info: dict[str, int | Decimal] = {
        "balance": app_manager.get_balance(addr=addr.addr),
        "energy": app_manager.get_energy_and_bandwidth(addr=addr.addr).get("energy"),
        "bandwidth": app_manager.get_energy_and_bandwidth(addr=addr.addr).get("bandwidth")
    }
    id = app_manager.save_address_info(data=cast(dict, {"address": addr.addr, **addr_info}), uow=unit_of_work.UnitOfWork())
    return {"id": id, **addr_info}


@app.get("/get_info_from_db")
def get_info_from_db(
        number: int = 10, page: int = 1, per_page: int = 10
) -> dict[str, int | list[dict[str, str |int | Decimal]]]:
    return app_manager.get_info_from_db(number=number, page=page, per_page=per_page, uow=unit_of_work.UnitOfWork())
