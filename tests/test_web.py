import dotenv
import os
from src.config import settings
from decimal import Decimal

import pytest

from src.entrypoints import web
from src.orm_tool.sql_aclchemy_wrapper import orm_conf

dotenv.load_dotenv()

print(settings.db_url)

def test_create_test_db():
    orm_conf.start_mapping()
    orm_conf.drop_tables()
    orm_conf.create_tables()

def test_get_address_info(test_client):
    response = test_client.post(url="https://127.0.0.1/address_info", json={"addr": os.getenv("ADDRESS")})
    json_result = response.json()
    assert response.status_code == 200
    assert isinstance(json_result["energy"], int)
    assert json_result["energy"] >= 0
    assert isinstance(json_result["bandwidth"], int)
    assert json_result["bandwidth"] >= 0
    assert isinstance(json_result["balance"], str)


# @pytest.mark.parametrize(
#     "number,page,per_page,total_pages,items",
#     (
#         5, 2, 2, 3, [{"id": 1, "address": os.getenv("ADDRESS"), "balance": Decimal("0"), "energy": 0, "bandwidth": 0}]
#     )
# )
def test_get_info_from_db(test_client):
    response = test_client.get(url="https://127.0.0.1/get_info_from_db")
    json_result = response.json()
    assert response.status_code == 200
    assert isinstance(json_result["page"], int)
    assert json_result["page"] > 0
    assert isinstance(json_result["per_page"], int)
    assert json_result["per_page"] > 0
    assert isinstance(json_result["total"], int)
    assert json_result["total"] > 0
    assert isinstance(json_result["total_pages"], int)
    assert json_result["total_pages"] > 0
    assert isinstance(json_result["items"][0]["balance"], str)
    assert isinstance(json_result["items"][0]["energy"], int)
    assert json_result["items"][0]["energy"] >= 0
    assert isinstance(json_result["items"][0]["bandwidth"], int)
    assert json_result["items"][0]["bandwidth"] >= 0