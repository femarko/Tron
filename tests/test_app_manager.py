import os
import dotenv
import psycopg2

from decimal import Decimal

from src.service_layer.app_manager import (
    get_energy_and_bandwidth,
    get_balance,
    save_address_info,
    get_info_from_db
)
from src.service_layer.unit_of_work import UnitOfWork
from src.orm_tool.sql_aclchemy_wrapper import orm_conf

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


def test_save_address_info():
    fake_data = {
        "address": "fake_address",
        "balance": 2000,
        "energy": 300,
        "bandwidth": 600
    }
    result = save_address_info(
        data=fake_data,
        uow=UnitOfWork(session_maker=orm_conf.session_maker)
    )
    pspg2_conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = pspg2_conn.cursor()
    with cursor as c:
        c.execute(
            f"SELECT * FROM address_bank"
        )
        fetched_data = c.fetchall()
    assert isinstance(result, int)
    assert result > 0
    assert len(fetched_data) == 1
    assert fetched_data[0][0] == result
    assert fetched_data[0][1] == fake_data["address"]
    assert fetched_data[0][2] == fake_data["balance"]
    assert fetched_data[0][3] == fake_data["energy"]
    assert fetched_data[0][4] == fake_data["bandwidth"]
