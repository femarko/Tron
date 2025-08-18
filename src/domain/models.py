from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import (
    Optional,
    TypeVar,
    Annotated
)


class DomainModelBase:
    save_date: Optional[datetime | str]

DomainModel = TypeVar("DomainModel", bound=DomainModelBase)


@dataclass
class AddressBank(DomainModelBase):
    address: Annotated[str, dict(unique=False), dict(nullable=False)]
    balance: Annotated[Decimal, dict(unique=False)]
    energy: Annotated[int, dict(unique=False)]
    bandwidth: Annotated[int, dict(unique=False)]
    id: Annotated[Optional[int], dict(primary_key=True), dict(autoincrement=True)] = None
    save_date: Annotated[Optional[datetime], dict(nullable=False), dict(server_default=datetime.now)] = None


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
