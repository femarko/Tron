import os
import dotenv
from decimal import Decimal

from src.application.app_manager import (
    get_energy_and_bandwidth,
    get_balance,
    save_address_info,
    get_info_from_db
)
from src.application.unit_of_work import UnitOfWork
from src.infrastructure.orm.sql_aclchemy_wrapper import orm_conf


dotenv.load_dotenv()


def test_get_energy_and_bandwidth():
    addr = os.getenv("ADDRESS")
    result = get_energy_and_bandwidth(addr=addr)
    assert isinstance(result, dict)
    assert "energy" in result
    assert "bandwidth" in result
    assert isinstance(result["energy"], int)
    assert isinstance(result["bandwidth"], int)


def test_get_balance():
    addr = os.getenv("ADDRESS")
    result = get_balance(addr=addr)
    assert isinstance(result, Decimal)
    assert result >= 0


def test_save_address_info(fake_data, pspg2_connection, drop_create_all):
    result = save_address_info(
        data=fake_data,
        uow=UnitOfWork(session_maker=orm_conf.session_maker)
    )
    with pspg2_connection:
        cursor = pspg2_connection.cursor()
        with cursor:
            cursor.execute("SELECT * FROM address_bank")
            fetched_data = cursor.fetchall()
    assert isinstance(result, int)
    assert result > 0
    assert len(fetched_data) == 1
    assert fetched_data[0][0] == result
    assert fetched_data[0][1] == fake_data["address"]
    assert fetched_data[0][2] == fake_data["balance"]
    assert fetched_data[0][3] == fake_data["energy"]
    assert fetched_data[0][4] == fake_data["bandwidth"]


def test_get_info_from_db(fake_data, pspg2_connection, drop_create_all, insert_fake_data):
    result = get_info_from_db(uow=UnitOfWork(session_maker=orm_conf.session_maker))
    assert isinstance(result, dict)
    assert result["page"] == 1
    assert result["per_page"] == 5
    assert result["total"] == 1
    assert result["total_pages"] == 1
    assert len(result["items"]) == 1
    assert isinstance(result["items"][0], dict)
    assert isinstance(result["items"][0]["id"], int)
    assert result["items"][0]["address"] == fake_data["address"]
    assert result["items"][0]["balance"] == fake_data["balance"]
    assert result["items"][0]["energy"] == fake_data["energy"]
    assert result["items"][0]["bandwidth"] == fake_data["bandwidth"]
