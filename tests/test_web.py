import dotenv
import os

from decimal import Decimal

from src.entrypoints import web

dotenv.load_dotenv()

def test_get_address_info(test_client):
    response = test_client.post(url="https://127.0.0.1/address_info", json={"addr": os.getenv("ADDRESS")})
    assert response.status_code == 200
    assert isinstance(response.json()["energy"], int)
    assert response.json()["energy"] >= 0
    assert isinstance(response.json()["bandwidth"], int)
    assert response.json()["bandwidth"] >= 0
    assert isinstance(response.json()["balance"], str)


def test_get_info_from_db(test_client):
    response = test_client.get(url="https://127.0.0.1/get_info_from_db")
    assert response.status_code == 200
    # assert isinstance(response.json()["number"], int)
    # assert response.json()["number"] > 0
    assert isinstance(response.json()["page"], int)
    assert response.json()["page"] > 0
    assert isinstance(response.json()["per_page"], int)
    assert response.json()["per_page"] > 0
    assert isinstance(response.json()["total"], int)
    assert response.json()["total"] > 0
    assert isinstance(response.json()["total_pages"], int)
    assert response.json()["total_pages"] > 0
    assert isinstance(response.json()["items"][0]["balance"], str)
    assert isinstance(response.json()["items"][0]["energy"], int)
    assert response.json()["items"][0]["energy"] >= 0
    assert isinstance(response.json()["items"][0]["bandwidth"], int)
    assert response.json()["items"][0]["bandwidth"] >= 0