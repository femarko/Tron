import pytest
from fastapi.testclient import TestClient
from sqlalchemy import orm, create_engine

from src.entrypoints import web
from src.orm_tool.sql_aclchemy_wrapper import session_maker
from src.service_layer.unit_of_work import UnitOfWork
from src.config import load_config


@pytest.fixture
def test_client():
    return TestClient(web.app)


@pytest.fixture
def set_test_conf():
    return load_config(mode="test")


@pytest.fixture
def unit_of_work():
    conf = load_config(mode="test")
    session_maker = orm.sessionmaker(bind=create_engine(conf.db_url))
    uow = UnitOfWork(session_maker=session_maker)
    return uow


## TODO: create fixture, returning unit of work, where session connects to test db
# TODO: create fixture, returning tron client with test network "nile"
# TODO: in tron_interface: make main network the default one
# TODO: create docker-compose.test.yaml, with test db and .env.test
# TODO: create .env.test
# TODO: '''create config, returning different settings depending on mode, passing as an environment variable value -
#  in order to run the app in test mode for testing it by Swagger UI, but not by Pytests'''