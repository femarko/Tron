import tronpy
from decimal import Decimal
from enum import Enum
from typing import (
    Optional,
    Type,
    cast,
    Callable
)

from src.infrastructure.tron.exceptions import tron_exc_mapper
from src.application.protocols import TronToolProto


class TronNetwork(str, Enum):
    SHASTA = "shasta"
    NILE = "nile"


class TronClient:
    def __init__(
            self,
            tron_tool: Callable[..., TronToolProto],
            network: Optional[TronNetwork] = None) -> None:
        if network:
            self.client = tron_tool(network=network)
        else:
            self.client = tron_tool()

    def get_energy_and_bandwidth(self, addr: str) -> dict[str, int]:
        try:
            resources = self.client.get_account_resource(addr=addr)
            energy = max(resources.get("EnergyLimit", 0) - resources.get("EnergyUsed", 0), 0)
            bandwidth = max(
                resources.get("NetLimit", 0) - resources.get("NetUsed", 0) + resources.get("freeNetLimit", 0), 0
            )
            return {"energy": energy, "bandwidth": bandwidth}
        except Exception as e:
            print(f"From TronClient.get_energy_and_bandwidth - Exception: {e = }")  # todo: remove
            raise tron_exc_mapper(exc=e) from e

    def get_balance(self, addr: str) -> Decimal:
        try:
            return self.client.get_account_balance(addr=addr)
        except Exception as e:
            raise tron_exc_mapper(exc=e) from e


def create_tron_client(mode: str) -> TronClient:
    if mode in {"test", "dev"}:
        return TronClient(
            tron_tool=cast(Type[TronToolProto], tronpy.Tron),
            network=TronNetwork.NILE
        )
    return TronClient(tron_tool=cast(Type[TronToolProto], tronpy.Tron))
