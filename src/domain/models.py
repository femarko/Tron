from datetime import datetime
from decimal import Decimal
from typing import (
    Optional,
    TypeVar
)


class DomainModelBase:
    save_date: Optional[datetime | str]

DomainModel = TypeVar("DomainModel", bound=DomainModelBase)

class AddressBank(DomainModelBase):
    def __init__(
            self,
            address: str,
            balance: int,
            energy: int,
            bandwidth: int,
            id: Optional[int] = None,
            save_date: Optional[datetime] = None
    ) -> None:
        self.id = id
        self.address = address
        self.balance = balance
        self.energy = energy
        self.bandwidth = bandwidth
        self.save_date = save_date


def create_addrbank_entry(**data) -> AddressBank:
    return AddressBank(**data)

def get_params(model: AddressBank) -> dict[str, str | int | Decimal]:
    return {
        "id": model.id,
        "address": model.address,
        "balance": model.balance,
        "energy": model.energy,
        "bandwidth": model.bandwidth
    }
