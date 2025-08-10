from dataclasses import dataclass
from typing import (
    Callable,
    TypeVar,
    Type,
    Generic
)

from src.bootstrap.config import (
    get_settings,
    Settings
)
from src.domain.models import DomainModel
from src.infrastructure.orm.repo_impl import create_address_repo
from src.infrastructure.tron.tron_interface import (
    create_tron_client,
    TronClient
)
from src.infrastructure.orm.sql_aclchemy_wrapper import ORMConf
from src.application.protocols import AddressBankRepoProto
from src.application.unit_of_work import UnitOfWork
from src.application.app_manager import (
    LoadAddressInfoFromTron,
    RetrieveAddressInfoFromDB
)
from src.domain.models import AddressBank

# DomainModel = TypeVar("DomainModel", bound=DomainModelBase)


@dataclass
class Container(Generic[DomainModel]):
    settings: Settings
    tron_client_maker: create_tron_client
    orm_conf: ORMConf
    # repo_creators: dict[Type[DomainModel], Callable[[Type[DomainModel]], AddressBankRepoProto]]
    uow: UnitOfWork
    load_address_info_from_tron_use_case: LoadAddressInfoFromTron
    retrieve_address_info_from_db_use_case: RetrieveAddressInfoFromDB

def build_container():
    settings = get_settings()
    tron_client_maker = create_tron_client
    orm_conf = ORMConf()
    repo_creators = {
        AddressBank: create_address_repo
    }
    uow = UnitOfWork(
        session_maker=orm_conf.session_maker,
        model_cls=AddressBank,
        repo_creators=repo_creators
    )
    load_address_info_from_tron_use_case = LoadAddressInfoFromTron(
        mode=settings.mode,
        tron_client_maker=tron_client_maker,
        uow=uow
    )
    retrieve_address_info_from_db_use_case = RetrieveAddressInfoFromDB(
        uow=uow
    )
    print(f"{settings.mode = }")  # todo: remove
    return Container(
        settings=settings,
        tron_client_maker=tron_client_maker,
        orm_conf=orm_conf,
        uow = uow,
        load_address_info_from_tron_use_case=load_address_info_from_tron_use_case,
        retrieve_address_info_from_db_use_case=retrieve_address_info_from_db_use_case
    )
