from enum import Enum
import tronpy


class TronNetwork(str, Enum):
    MAINNET = "mainnet"
    TESTNET = "testnet"
    SHASTA = "shasta"
    NILE = "nile"


class TronClient:
    def __init__(self, network: TronNetwork = TronNetwork.NILE) -> None:
        self.client = tronpy.Tron(network=network)

    def get_energy(self, addr: str) -> dict[str, int]:
        resources = self.client.get_account_resource(addr=addr)
        energy = max(resources.get("EnergyLimit", 0) - resources.get("EnergyUsed", 0), 0)
        bandwidth = max(
            resources.get("NetLimit", 0) - resources.get("NetUsed", 0) + resources.get("FreeNetLimit", 0), 0
        )
        return {"energy": energy, "bandwidth": bandwidth}