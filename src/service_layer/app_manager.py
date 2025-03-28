from decimal import Decimal

import src.tron_interface as tr


def get_energy_and_bandwidth(addr: str, network: tr.Optional[tr.TronNetwork]) -> dict[str, int]:
    tron_client = tr.create_tron_client(network=network)
    return tron_client.get_energy_and_bandwidth(addr=addr)

def get_balance(addr: str, network: tr.Optional[tr.TronNetwork]) -> Decimal:
    tron_client = tr.create_tron_client(network=network)
    return tron_client.get_balance(addr=addr)

def save_address_info(**data) -> None:
    pass
