import os
import tronpy


def get_tron_addr_energy(network: str, addr: str) -> dict[str, str]:

    return blch_interface.get_account_resource(addr=addr)

def get_address_info(blch_interface, addr: str) -> dict[str, str]:
    return blch_interface.get_account(addr=addr)


def get_energy(blch_interface, addr: str) -> dict[str, str]:
    resources = blch_interface.get_account_resource(addr=os.getenv("ADDRESS"))

    blch_interface.get_account_resource(addr=addr)


client = tronpy.Tron(network="nile")
wallet = client.generate_address()
info = client.get_account(addr=os.getenv("ADDRESS"))
bal = client.get_account_balance(addr=str(wallet["base58check_address"]))