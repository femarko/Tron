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

class Person(BaseModel):
    person: str


@app.post("/address_info")
def get_address_info(
        addr: str = fastapi.Body(..., embed=True),
) -> dict[str, int | Decimal]:
    addr_info: dict[str, int | Decimal] = {
        "balance": app_manager.get_balance(addr=addr),
        "energy": app_manager.get_energy_and_bandwidth(addr=addr).get("energy"),
        "bandwidth": app_manager.get_energy_and_bandwidth(addr=addr).get("bandwidth")
    }
    id = app_manager.save_address_info(data=cast(dict, {"address": addr, **addr_info}), uow=unit_of_work.UnitOfWork())
    return {"id": id, **addr_info}
