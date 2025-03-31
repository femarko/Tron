from decimal import Decimal
from enum import Enum
from typing import Optional

import tronpy

class TronNetwork(str, Enum):
    SHASTA = "shasta"
    NILE = "nile"


class TronClient:
    def __init__(self, network: Optional[TronNetwork] = TronNetwork.NILE) -> None:
        self.client = tronpy.Tron(network=network)

    def get_energy_and_bandwidth(self, addr: str) -> dict[str, int]:
        resources = self.client.get_account_resource(addr=addr)
        energy = max(resources.get("EnergyLimit", 0) - resources.get("EnergyUsed", 0), 0)
        bandwidth = max(
            resources.get("NetLimit", 0) - resources.get("NetUsed", 0) + resources.get("freeNetLimit", 0), 0
        )
        return {"energy": energy, "bandwidth": bandwidth}

    def get_balance(self, addr: str) -> Decimal:
        return self.client.get_account_balance(addr=addr)


def create_tron_client(network: Optional[TronNetwork] = TronNetwork.NILE) -> TronClient:
    return TronClient(network=network)
