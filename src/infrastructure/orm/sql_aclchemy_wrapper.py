import dataclasses

from sqlalchemy import create_engine, orm, Table, Column, Integer, String, DECIMAL,DateTime, func
from sqlalchemy.exc import IntegrityError
from functools import lru_cache

from src.domain.models import AddressBank
from src.bootstrap.config import settings


engine = create_engine(settings.db_url)
session_maker = orm.sessionmaker(bind=engine)
table_mapper = orm.registry()

address_bank_table = Table(
    "address_bank",
    table_mapper.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("address", String(200), index=True, nullable=False),
    Column("balance", DECIMAL, index=True, nullable=False),
    Column("energy", Integer, index=True, nullable=False),
    Column("bandwidth", Integer, index=True, nullable=False),
    # Column("create_time", DateTime, nullable=False),
    Column("save_date", DateTime, server_default=func.now(), nullable=False)
)


@dataclasses.dataclass
class ORMConf:
    integrity_error = IntegrityError
    engine = engine
    session_maker = session_maker

    @staticmethod
    @lru_cache
    def start_mapping():
        print("Start mapping...")
        table_mapper.map_imperatively(class_=AddressBank, local_table=address_bank_table)

    def create_tables(self):
        print("Creating tables...")
        table_mapper.metadata.create_all(bind=self.engine)

    def drop_tables(self):
        print("Dropping tables...")
        table_mapper.metadata.drop_all(bind=self.engine)


orm_conf = ORMConf()
