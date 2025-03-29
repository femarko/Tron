from datetime import datetime
from typing import Optional


class AddressBank:
    def __init__(
            self,
            address: str,
            balance: int,
            available_energy: int,
            create_time: datetime,
            id: Optional[int] = None,
            save_date: Optional[datetime] = None
    ) -> None:
        self.id = id
        self.address = address
        self.balance = balance
        self.available_energy = available_energy
        self.create_time = create_time
        self.save_date = save_date


def create_addrbank_entry(**data) -> AddressBank:
    return AddressBank(**data)
