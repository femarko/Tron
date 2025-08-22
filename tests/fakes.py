import os
from decimal import Decimal
from typing import Optional

from src.application.protocols import (
    TronClientProto,
    AddressBankRepoProto,
    UoWProto
)
from src.domain.models import AddressBank


fake_address_info = {
    "id": None,
    "address": os.getenv("ADDRESS"),
    "balance": Decimal(2000),
    "energy": 300,
    "bandwidth": 400,
}
fake_tron_lib_data = {
    "EnergyLimit": 100,
    "EnergyUsed": 50,
    "NetLimit": 200,
    "NetUsed": 100,
    "balance": Decimal(2000)
}


class FakeTronLib:
    def __init__(
            self,
            fake_data: dict[str, str | int | Decimal],
            network: Optional[str] = None
    ) -> None:
        super().__init__()
        self.fake_data = fake_data
        self.network = network

    def get_account_resource(self, addr: str) -> dict[str, int]:
        return {
            "EnergyLimit": self.fake_data.get("EnergyLimit", 0),
            "EnergyUsed": self.fake_data.get("EnergyUsed", 0),
            "NetLimit": self.fake_data.get("NetLimit", 0),
            "NetUsed": self.fake_data.get("NetUsed", 0),
        }

    def get_account_balance(self, addr: str) -> Decimal:
        return self.fake_data.get("balance")


class FakeTronClient(TronClientProto):
    def __init__(self, address_info: dict[str, str | int | Decimal]) -> None:
        self.address_info = address_info

    def get_energy_and_bandwidth(self, addr: str) -> dict[str, int]:
        return {
            "energy": self.address_info.get("energy"),
            "bandwidth": self.address_info.get("bandwidth"),
        }

    def get_balance(self, addr: str) -> Decimal:
        return Decimal(self.address_info.get("balance"))

class FakeRepo(AddressBankRepoProto):
    def __init__(self, address_info: dict[str, str | int | Decimal]) -> None:
        self.address_info = address_info

    def add(self, instance: AddressBank) -> None:
        pass

    def get(self, instance_id: int) -> AddressBank:
        return AddressBank(**self.address_info)

    def get_recent(
            self,
            limit_total: int,
            page: int,
            per_page: int
    ) -> dict[str, int | list[dict[str, str | int | Decimal]]]:
        return {
            "page": page,
            "per_page": per_page,
            "total": 1,
            "total_pages": 1,
            "items": [{**self.address_info}]
        }

    def delete(self, instance: AddressBank) -> None:
        pass


class FakeUoW(UoWProto):
    def __enter__(self) -> "FakeUoW": ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...

    def commit(self) -> None:
        pass

    def flush(self):
        pass

    def rollback(self) -> None:
        pass

    @property
    def repo(self) -> AddressBankRepoProto:
        return FakeRepo(address_info=fake_address_info)
