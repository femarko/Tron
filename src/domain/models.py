from dataclasses import (
    dataclass,
)
from datetime import datetime
from decimal import Decimal
from typing import (
    Optional,
    TypeVar,
    Annotated,
)
from src.domain.exceptions import UnexpectedParams



class DomainModelBase:
    save_date: Optional[datetime | str]


DomainModel = TypeVar("DomainModel", bound=DomainModelBase)


@dataclass
class AddressBank(DomainModelBase):
    address: Annotated[str, dict(unique=False), dict(nullable=False)]
    balance: Annotated[Decimal, dict(unique=False), dict(nullable=False)]
    energy: Annotated[int, dict(unique=False), dict(nullable=False)]
    bandwidth: Annotated[int, dict(unique=False), dict(nullable=False)]
    id: Annotated[Optional[int], dict(primary_key=True), dict(autoincrement=True)] = None
    save_date: Annotated[Optional[datetime], dict(nullable=False), dict(server_default=datetime.now)] = None

    @classmethod
    def _validate_input_data(cls, **data):
        validators = {
            "'data' must contain 'address', 'balance', 'energy', 'bandwidth'": lambda: all(
                data.get(key) is not None for key in ("address", "balance", "energy", "bandwidth")
            ),
            "'address' must comply with the Tron format.": lambda: isinstance(data.get("address"), str)
               and data.get("address").startswith("T")
               and 30 <= len(data.get("address")) <= 35,
            "'balance', 'energy', 'bandwidth' cannot be negative": lambda: all(
                item >=0 for item in (
                    data.get("balance"),
                    data.get("energy"),
                    data.get("bandwidth")
                )
            )
        }
        errors = [msg for msg, fn in validators.items() if not fn()]
        if errors:
            raise UnexpectedParams(
                message="\n".join(f"{i + 1}. {msg}" for i, msg in enumerate(errors))
            )

    @classmethod
    def create(cls, **data) -> "AddressBank":
      cls._validate_input_data(**data)
      return cls(
        address=data["address"],
        balance=data["balance"],
        energy=data["energy"],
        bandwidth=data["bandwidth"],
        save_date=datetime.now()
    )


def get_params(model: AddressBank) -> dict[str, str | int | Decimal]:
    return {
        "address": model.address,
        "balance": model.balance,
        "energy": model.energy,
        "bandwidth": model.bandwidth,
        "id": model.id
    }
