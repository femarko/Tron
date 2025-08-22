import pytest

from src.application.use_cases import (
    LoadAddressInfoFromTron,
    RetrieveAddressInfoFromDB
)


def test_loads_address_info_from_fake_tron_client(
        fake_tron_client_maker,
        fake_uow,
        get_fake_address_info
):
    use_case = LoadAddressInfoFromTron(
        mode="test",
        tron_client_maker=fake_tron_client_maker,
        uow=fake_uow
    )
    result = use_case.execute(addr=get_fake_address_info["address"])
    expected = {**get_fake_address_info}
    for key, value in expected.items():
        assert result[key] == value, f"Expected '{key}': {value}, got: {result[key]}."


def test_retrieves_address_info_from_db(
        fake_uow,
        get_fake_address_info
):
    use_case = RetrieveAddressInfoFromDB(uow=fake_uow)
    result = use_case.execute(
        number=1,
        page=1,
        per_page=1
    )
    expected = {
        "page": 1,
        "per_page": 1,
        "total_pages": 1,
        "items": [{**get_fake_address_info}]
    }
    for key, value in expected.items():
        assert result[key] == value, f"Expected '{key}': {value}, got: {result[key]}."
