import dataclasses
import pathlib

from sqlalchemy import create_engine, orm, Table, Column, Integer, String, DateTime, func
from sqlalchemy.exc import IntegrityError

from src.domain import AddressBank


db_path = pathlib.Path(__file__).parent.parent / "db/zuzu.db"
engine = create_engine(f"sqlite:///{db_path}")
session_maker = orm.sessionmaker(bind=engine)
table_mapper = orm.registry()

address_bank_table = Table(
    "address_bank",
    table_mapper.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("address", String(200), index=True, nullable=False),
    Column("balance", String(200), index=True, nullable=False),
    Column("energy", String(200), index=True, nullable=False),
    Column("create_time", DateTime, nullable=False),
    Column("save_date", DateTime, server_default=func.now(), nullable=False)
)


@dataclasses.dataclass
class ORMConf:
    integrity_error = IntegrityError
    engine = engine
    session_maker = session_maker

    @staticmethod
    def start_mapping():
        table_mapper.map_imperatively(class_=AddressBank, local_table=address_bank_table)

    def create_tables(self):
        table_mapper.metadata.create_all(bind=self.engine)


orm_conf = ORMConf()
