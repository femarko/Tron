import datetime
from typing import Optional

import tronpy

import os

from dotenv import load_dotenv

load_dotenv()

client = tronpy.Tron(network="nile")
wallet = client.generate_address()
# client.create_account(wallet["base58check_address"])
info = client.get_account(addr=os.getenv("ADDRESS"))
resources = client.get_account_resource(addr=os.getenv("ADDRESS"))

bal = client.get_account_balance(addr=str(wallet["base58check_address"]))
pass


class AddressBank:
    def __init__(
            self,
            address,
            balance,
            available_energy,
            create_time,
            id: Optional[int] = None,
            save_date: Optional[datetime] = None
    ):
        self.id = id
        self.address = address
        self.balance = balance
        self.available_energy = available_energy
        self.create_time = create_time
        self.save_date = save_date


def save_address_info(**data):
    return AddressBank(**data)


def get_address_info(blch_interface, addr: str) -> dict[str, str]:
    return blch_interface.get_account(addr=addr)

