import pytest

from src.infrastructure.tron.tron_interface import (
    TronClient,
    TronNetwork
)
from src.infrastructure.tron.exceptions import TronError
from tests.fakes import (
    FakeTronLib,
    fake_tron_lib_data,
    fake_tron_exception_types,
    FakeTronException
)
from src.domain.exceptions import NotFoundError


def test_tron_interface_creates_tron_client_with_the_network_passed_as_argument():
    tron_client = TronClient(
        tron_tool=lambda network: FakeTronLib(fake_data=fake_tron_lib_data, network=network),
        network=TronNetwork.NILE,
        exception_types=fake_tron_exception_types
    )
    assert isinstance(tron_client.client, FakeTronLib), \
        f"Expected: type(tron_client.client) = FakeTronLib, got: {type(tron_client.client) = }."
    assert tron_client.client.network == TronNetwork.NILE, \
        f"Expected: tron_client.client.network = TronNetwork.NILE, got: {tron_client.client.network = }."


def test_tron_interface_creates_tron_client_with_mainnet_when_network_argument_is_not_passed():
    tron_client = TronClient(
        tron_tool=lambda: FakeTronLib(fake_data=fake_tron_lib_data),
        exception_types=fake_tron_exception_types
    )
    assert isinstance(tron_client.client, FakeTronLib), \
        f"Expected: type(tron_client.client) = FakeTronLib, got: {type(tron_client.client) = }."
    assert tron_client.client.network == TronNetwork.MAINNET, \
        f"Expected: tron_client.client.network = TronNetwork.MAINNET, got: {tron_client.client.network = }."


def test_tron_interface_raises_error_when_invalid_network_is_passed():
    with pytest.raises(TronError) as e:
        TronClient(
            tron_tool=lambda network: FakeTronLib(fake_data=fake_tron_lib_data, network=network),
            network="invalid",  # type: ignore
            exception_types=fake_tron_exception_types
        )
    assert e.value.message == "Invalid network: invalid."


def test_tron_interface_returns_energy_and_bandwidth_using_fake_tron_lib():
    tron_client = TronClient(
        tron_tool=lambda network: FakeTronLib(fake_data=fake_tron_lib_data, network=network),
        network=TronNetwork.NILE,
        exception_types=fake_tron_exception_types
    )
    expected = {
        "energy": fake_tron_lib_data.get("EnergyLimit", 0) - fake_tron_lib_data.get("EnergyUsed", 0),
        "bandwidth": fake_tron_lib_data.get("NetLimit", 0)
                     - fake_tron_lib_data.get("NetUsed", 0)
                     + fake_tron_lib_data.get("freeNetLimit", 0)
    }
    result = tron_client.get_energy_and_bandwidth("test_address")
    assert result["energy"] == expected["energy"], \
        f"Expected: result['energy'] = {expected['energy']}, got: {result['energy']}."
    assert result["bandwidth"] == expected["bandwidth"], \
        f"Expected: result['bandwidth'] = {expected['bandwidth']}, got: {result['bandwidth']}."


def test_tron_interface_returns_balance_using_fake_tron_lib():
    tron_client = TronClient(
        tron_tool=lambda network: FakeTronLib(fake_data=fake_tron_lib_data, network=network),
        network=TronNetwork.NILE,
        exception_types=fake_tron_exception_types
    )
    expected = fake_tron_lib_data.get("balance")
    result = tron_client.get_balance("test_address")
    assert result == expected, f"Expected: result = {expected}, got: {result}."


def test_tron_interface_mapps_tron_exceptions_using_fake_tron_lib():
    tron_client = TronClient(
        tron_tool=lambda network: FakeTronLib(fake_data=fake_tron_lib_data, network=network),
        network=TronNetwork.NILE,
        exception_types=fake_tron_exception_types
    )
    with pytest.raises(NotFoundError):
        tron_client.get_energy_and_bandwidth(addr="test_exception_raising")
