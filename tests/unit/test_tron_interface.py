from src.infrastructure.tron.tron_interface import (
    TronClient,
    TronNetwork
)
from tests.fakes import FakeTronLib, fake_tron_lib_data


# fake_tron_lib = FakeTronLib(fake_data=fake_tron_lib_data)

def test_tron_interface_creates_tron_client_with_different_networks():
    tron_client = TronClient(
        tron_tool=lambda network: FakeTronLib(fake_data=fake_tron_lib_data),
        network=TronNetwork.NILE
    )
    assert tron_client.client.network == TronNetwork.NILE