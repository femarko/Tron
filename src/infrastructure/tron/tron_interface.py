import tronpy
from tronpy.exceptions import (
    BadAddress,
    BadKey,
    BadSignature,
    BadHash,
    TaposError,
    UnknownError,
    TransactionError,
    TvmError,
    ValidationError,
    ApiError,
    NotFound,
    AddressNotFound,
    TransactionNotFound,
    BlockNotFound,
    AssetNotFound,
    DoubleSpending,
    BugInJavaTron
)

from decimal import Decimal
from enum import Enum
from typing import Optional

from src.bootstrap.config import get_settings
from src.domain.errors import TronError


class TronNetwork(str, Enum):
    SHASTA = "shasta"
    NILE = "nile"


TRON_ERRORS = (
    BadAddress,
    BadKey,
    BadSignature,
    BadHash,
    TaposError,
    UnknownError,
    TransactionError,
    TvmError,
    ValidationError,
    ApiError,
    NotFound,
    AddressNotFound,
    TransactionNotFound,
    BlockNotFound,
    AssetNotFound,
    DoubleSpending,
    BugInJavaTron
)

class TronClient:
    def __init__(self, network: Optional[TronNetwork] = None) -> None:
        if network:
            self.client = tronpy.Tron(network=network)
        else:
            self.client = tronpy.Tron()

    def get_energy_and_bandwidth(self, addr: str) -> dict[str, int]:
        try:
            resources = self.client.get_account_resource(addr=addr)
            energy = max(resources.get("EnergyLimit", 0) - resources.get("EnergyUsed", 0), 0)
            bandwidth = max(
                resources.get("NetLimit", 0) - resources.get("NetUsed", 0) + resources.get("freeNetLimit", 0), 0
            )
            return {"energy": energy, "bandwidth": bandwidth}
        except TRON_ERRORS as e:
            raise TronError(message=str(e)) from e

    def get_balance(self, addr: str) -> Decimal:
        try:
            return self.client.get_account_balance(addr=addr)
        except TRON_ERRORS as e:
            raise TronError(message=str(e)) from e


def create_tron_client(mode: str) -> TronClient:
    if mode in {"test", "dev"}:
        print(f"From create_tron_client: {get_settings().mode = }")  # todo: remove
        return TronClient(network=TronNetwork.NILE)
    return TronClient()
