import pytest
import os
import psycopg2
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from decimal import Decimal
from typing import (
    Callable,
    TypeVar
)
from dataclasses import dataclass

from src.infrastructure.tron.tron_interface import (
    create_tron_client
)
from src.interfaces.fastapi_app import main
from src.bootstrap.bootstrap import container
from src.application.protocols import AddressBankRepoProto, UoWProto, TronClientProto
from src.domain.models import AddressBank

load_dotenv()

fake_address_info = {
    "id": None,
    "address": os.getenv("ADDRESS"),
    "balance": Decimal(2000),
    "energy": 300,
    "bandwidth": 400,
}


@pytest.fixture
def get_fake_address_info() -> dict[str, str | int | Decimal]:
    return fake_address_info


class FakeTronClient(TronClientProto):
    def __init__(self, address_info: dict[str,  str | int| Decimal]) -> None:
        self.address_info = address_info

    def get_energy_and_bandwidth(self, addr: str) -> dict[str, int]:
        return {
            "energy": self.address_info.get("energy"),
            "bandwidth": self.address_info.get("bandwidth"),
        }

    def get_balance(self, addr: str) -> Decimal:
        return Decimal(self.address_info.get("balance"))


class FakeRepo(AddressBankRepoProto):
    def __init__(self) -> None:
        self.fake_address_info = fake_address_info

    def add(self, instance: AddressBank) -> None:
        pass

    def get(self, instance_id: int) -> AddressBank:
        return AddressBank(**self.fake_address_info)

    def get_recent(
            self,
            limit_total: int,
            page: int,
            per_page: int
    ) -> dict[str, int | list[dict[str, str | int | Decimal]]]:
        return {
            "page": page,
            "per_page": per_page,
            "total": 1,
            "total_pages": 1,
            "items": [{**self.fake_address_info}]
        }

    def delete(self, instance: AddressBank) -> None:
        pass


class FakeUoW(UoWProto):
    def __enter__(self) -> "FakeUoW": ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...

    def commit(self) -> None:
        pass

    def flush(self):
        pass

    def rollback(self) -> None:
        pass

    @property
    def repo(self) -> AddressBankRepoProto:
        return FakeRepo()


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



