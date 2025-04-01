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



def test_get_info_from_db(): pass  # TODO: implement test