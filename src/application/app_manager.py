from decimal import Decimal

import src.infrastructure.tron.tron_interface as tr
import src.domain.models as models
from src.application.unit_of_work import UnitOfWork
from src.bootstrap.config import settings


def get_energy_and_bandwidth(addr: str) -> dict[str, int]:
    if settings.mode in {"test", "dev"}:
        return tr.create_tron_client(network=tr.TronNetwork.NILE).get_energy_and_bandwidth(addr=addr)
    return tr.create_tron_client().get_energy_and_bandwidth(addr=addr)

def get_balance(addr: str) -> Decimal:
    if settings.mode in {"test", "dev"}:
        return tr.create_tron_client(network=tr.TronNetwork.NILE).get_balance(addr=addr)
    return tr.create_tron_client().get_balance(addr=addr)

def save_address_info(data: dict[str, str | int | Decimal], uow: UnitOfWork) -> int:
    entry = models.create_addrbank_entry(**data)
    with uow:
        uow.address_repo.add(entry)
        uow.commit()
        return entry.id

def get_info_from_db(uow: UnitOfWork,
                     number: int = 20,
                     page: int = 1,
                     per_page: int = 5) -> dict[str, int | list[dict[str, str | int | Decimal]]]:
    with uow:
        result = uow.address_repo.get_recent(number=number, page=page, per_page=per_page)
    return result
