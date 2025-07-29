import pytest
import os
import psycopg2
from fastapi.testclient import TestClient

from src.infrastructure.tron.tron_interface import (
    TronNetwork,
    create_tron_client
)
from src.interfaces.fastapi_app import main
from src.infrastructure.orm.sql_aclchemy_wrapper import orm_conf
from src.config import settings


@pytest.fixture
def test_client():
    return TestClient(main.app)


@pytest.fixture(scope="function")
def drop_create_all():
    if settings.mode == "test":
        orm_conf.start_mapping()
        orm_conf.drop_tables()
        orm_conf.create_tables()
    yield
    if settings.mode == "test":
        orm_conf.drop_tables()


@pytest.fixture
def fake_data():
    fake_data = {
        "address": "fake_address",
        "balance": 2000,
        "energy": 300,
        "bandwidth": 600
    }
    return fake_data


@pytest.fixture
def pspg2_connection():
    pspg2_conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    return pspg2_conn


@pytest.fixture
def insert_fake_data(fake_data, pspg2_connection):
    with pspg2_connection:
        cursor = pspg2_connection.cursor()
        with cursor:
            cursor.execute(
                query="INSERT INTO address_bank (address, balance, energy, bandwidth) VALUES (%s, %s, %s, %s)",
                vars=(fake_data["address"], fake_data["balance"], fake_data["energy"], fake_data["bandwidth"])
            )


@pytest.fixture
def tron_client_nile():
    return create_tron_client(network=TronNetwork.NILE)