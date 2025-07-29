import os
import dotenv
import tronpy

from decimal import Decimal

from src.infrastructure.tron import tron_interface

dotenv.load_dotenv()

def test_create_tron_client():
    tron_client = tron_interface.create_tron_client()
    assert isinstance(tron_client, tron_interface.TronClient)
    assert isinstance(tron_client.client, tronpy.Tron)


def test_get_energy_and_bandwidth(tron_client_nile):
    energy_and_bandwidth = tron_client_nile.get_energy_and_bandwidth(addr=os.getenv("ADDRESS"))
    assert isinstance(energy_and_bandwidth, dict)
    assert "energy" in energy_and_bandwidth
    assert "bandwidth" in energy_and_bandwidth
    assert isinstance(energy_and_bandwidth["energy"], int)
    assert isinstance(energy_and_bandwidth["bandwidth"], int)


def test_get_balance(tron_client_nile):
    balance = tron_client_nile.get_balance(addr=os.getenv("ADDRESS"))
    assert isinstance(balance, Decimal)
    assert balance >= 0
