import pytest
from fastapi.testclient import TestClient
from sqlalchemy import orm, create_engine

from src.entrypoints import web
from src.service_layer.unit_of_work import UnitOfWork
from src.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.config import settings


@pytest.fixture
def test_client():
    return TestClient(web.app)


@pytest.fixture(autouse=True, scope="session")
def create_drop_all():
    if settings.mode == "test":
        orm_conf.start_mapping()
        orm_conf.drop_tables()
        orm_conf.create_tables()
    yield
    if settings.mode == "test":
        orm_conf.drop_tables()


# TODO: create fixture, returning tron client with test network "nile"
# TODO: in tron_interface: make main network the default one
# TODO: create docker-compose.test.yaml, with test db and .env.test
# TODO: create .env.test
# TODO: '''create config, returning different settings depending on mode, passing as an environment variable value -
#  in order to run the app in test mode for testing it by Swagger UI, but not by Pytests'''