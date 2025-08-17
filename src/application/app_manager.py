from decimal import Decimal
from typing import Callable

from src.application.protocols import (
    TronClientProto,
    UoWProto
)
from src.domain.models import (
    AddressBank,
    create_addrbank_entry
)


class LoadAddressInfoFromTron:
    def __init__(
            self,
            mode: str,
            tron_client_maker: Callable[..., TronClientProto],
            uow: UoWProto
    ) -> None:
        self.uow = uow
        self.tron_client = tron_client_maker(mode=mode)

    def execute(self, addr: str,) -> dict[str, int]:
        energy_and_bandwidth: dict[str, int] = self.tron_client.get_energy_and_bandwidth(addr=addr)
        balance: Decimal = self.tron_client.get_balance(addr=addr)
        addr_info: dict[str, str | int | Decimal] = {
            "address": addr,
            "balance": balance,
            "energy": energy_and_bandwidth.get("energy"),
            "bandwidth": energy_and_bandwidth.get("bandwidth")
        }
        entry: AddressBank = create_addrbank_entry(**addr_info)
        with self.uow:
            self.uow.repo.add(entry)
            self.uow.flush()
            new_entry_id: int = entry.id
            self.uow.commit()
            return {
                "id": new_entry_id,
                **addr_info
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
        with self.uow:
            result: dict[str, int | list[dict[str, str | int | Decimal]]] = self.uow.repo.get_recent(
                limit_total=number, page=page, per_page=per_page
            )
        return result
