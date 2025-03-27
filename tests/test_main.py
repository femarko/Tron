import tronpy
import pytest
from fastapi.testclient import TestClient

from src import exper_1

wallet_address = tronpy.Wallet().address

client = TestClient(app)

def test_get_wallet_info():
    response = client.post("/wallet", json={"address": wallet_address})
    assert response.status_code == 200
    assert response.json() == {"address": wallet_address, "bandwidth": 0, "energy": 0, "balance": 0}