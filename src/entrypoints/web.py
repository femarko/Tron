from decimal import Decimal

import fastapi
from fastapi.params import Depends
from typing import cast

from src.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.service_layer import app_manager, unit_of_work


app = fastapi.FastAPI()
orm_conf.start_mapping()


@app.post("/address_info")
def get_address_info(
        addr: str,
        en_band = Depends(app_manager.get_energy_and_bandwidth),
        balance = Depends(app_manager.get_balance),
        uow = Depends(unit_of_work.UnitOfWork)
) -> dict[str, int | Decimal]:
    addr_info: dict[str, int | Decimal] = {
        "balance": balance,
        "available_energy": en_band.get("energy"),  # type: ignore
        "bandwidth": en_band.get("bandwidth")  # type: ignore
    }
    id = app_manager.save_address_info(data={"address": addr, **addr_info}, uow=cast(unit_of_work.UnitOfWork, uow))
    return {"id": id, **addr_info}


