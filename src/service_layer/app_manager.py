from decimal import Decimal

import src.tron_interface as tr
import src.domain.models as models
from src.service_layer.unit_of_work import UnitOfWork


def get_energy_and_bandwidth(addr: str) -> dict[str, int]:
    tron_client = tr.create_tron_client()
    return tron_client.get_energy_and_bandwidth(addr=addr)

def get_balance(addr: str) -> Decimal:
    tron_client = tr.create_tron_client()
    return tron_client.get_balance(addr=addr)

def save_address_info(data: dict[str, str | int | Decimal], uow: UnitOfWork) -> int:
    entry = models.create_addrbank_entry(**data)
    with uow:
        uow.address_repo.add(entry)
        uow.commit()
        return entry.id

def get_info_from_db(number: int, page: int, per_page: int, uow: UnitOfWork) -> dict[str, int | list[dict[str, str | int | Decimal]]]:
    with uow:
        result = uow.address_repo.get_recent(number=number, page=page, per_page=per_page)
    return result
