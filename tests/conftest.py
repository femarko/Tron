import pytest
import os
import psycopg2
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from decimal import Decimal
from typing import (
    Callable
)

from src.interfaces.fastapi_app import main
from src.bootstrap.bootstrap import container
from src.application.protocols import TronClientProto
from tests.fakes import fake_address_info, FakeTronClient, FakeRepo, FakeUoW

load_dotenv()


@pytest.fixture
def get_fake_address_info() -> dict[str, str | int | Decimal]:
    return fake_address_info


@pytest.fixture
def fake_uow() -> FakeUoW:
    return FakeUoW()


@pytest.fixture
def fake_repo() -> FakeRepo:
    return FakeRepo()


@pytest.fixture
def fake_tron_client_maker(get_fake_address_info) -> Callable[..., TronClientProto]:
    def _maker(mode: str) -> TronClientProto:
        return FakeTronClient(address_info=get_fake_address_info)
    return _maker


@pytest.fixture
def test_client():
    return TestClient(main.app)


@pytest.fixture(scope="function")
def drop_create_all():
    if container.mode == "test":
        container.orm_conf.start_mapping()
        container.orm_conf.drop_tables()
        container.orm_conf.create_tables()
    yield
    if container.mode == "test":
        container.orm_conf.drop_tables()


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


# @pytest.fixture
# def tron_client_nile():
#     return create_tron_client(mode=container.settings.mode)



