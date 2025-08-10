from decimal import Decimal
from typing import Callable

from src.infrastructure.tron.tron_interface import (
    TronClient,
    TronNetwork
)
import src.domain.models as models
from src.application.protocols import UoWProto


class LoadAddressInfoFromTron:
    def __init__(
            self,
            mode: str,
            tron_client_maker: Callable[..., TronClient],
            uow: UoWProto
    ) -> None:
        self.mode = mode
        self.tron_client_maker = tron_client_maker
        self.uow = uow

    def execute(self, addr: str,) -> dict[str, int]:
        if self.mode in {"test", "dev"}:
            tron_client = self.tron_client_maker(network=TronNetwork.NILE)
            print("NILE")  # todo remove
        else:
            tron_client = self.tron_client_maker()
            print("not NILE")  # todo remove
        energy_and_bandwidth: dict[str, int] = tron_client.get_energy_and_bandwidth(addr=addr)
        entry: models.AddressBank = models.create_addrbank_entry(**energy_and_bandwidth)
        with self.uow:
            self.uow.repo.add(entry)
            self.uow.flush()
            new_entry_id: int = entry.id
            self.uow.commit()
            return {
                "id": new_entry_id,
                **energy_and_bandwidth
            }


class RetrieveAddressInfoFromDB:
    def __init__(
            self,
            uow: UoWProto,
    ) -> None:
        self.uow = uow

    def execute(
            self,
            number: int = 20,
            page: int = 1,
            per_page: int = 5
    ) -> dict[str, int | list[dict[str, str | int | Decimal]]]:
        return self.uow.repo.get_recent(
            number=number,
            page=page,
            per_page=per_page
        )


# def get_energy_and_bandwidth(addr: str) -> dict[str, int]:
#     if settings.mode in {"test", "dev"}:
#         return tr.create_tron_client(network=tr.TronNetwork.NILE).get_energy_and_bandwidth(addr=addr)
#     return tr.create_tron_client().get_energy_and_bandwidth(addr=addr)
#
# def get_balance(addr: str) -> Decimal:
#     if settings.mode in {"test", "dev"}:
#         return tr.create_tron_client(network=tr.TronNetwork.NILE).get_balance(addr=addr)
#     return tr.create_tron_client().get_balance(addr=addr)
#
# def save_address_info(data: dict[str, str | int | Decimal], uow: UnitOfWork) -> int:
#     entry = models.create_addrbank_entry(**data)
#     with uow:
#         uow.address_repo.add(entry)
#         uow.commit()
#         return entry.id
#
# def get_info_from_db(uow: UnitOfWork,
#                      number: int = 20,
#                      page: int = 1,
#                      per_page: int = 5) -> dict[str, int | list[dict[str, str | int | Decimal]]]:
#     with uow:
#         result = uow.address_repo.get_recent(number=number, page=page, per_page=per_page)
#     return result
