from dataclasses import (
    dataclass,
    field
)
from typing import (
    Callable,
    Iterable,
    Type,
    TypeVar,
    get_args,
    Optional,
    Generic,
    Any
)
from datetime import datetime
from sqlalchemy import (
    create_engine,
    orm,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    func,
    desc as sa_desc
)
from sqlalchemy.orm import (
    aliased,
    sessionmaker as sa_session_maker
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine.base import Engine

from src.application.protocols import SessionProto
from src.domain.models import DomainModelBase
from src.domain.errors import DBError
from src.infrastructure.orm.adapters import (
    SQLAlchemyQueryAdapter,
    SQLAlchemySessionAdapter
)


T = TypeVar("T")

@dataclass
class ORMConf(Generic[T]):
    _db_url: str
    _domain_models: Iterable[T]
    _engine: Engine = field(init=False)
    integrity_error: IntegrityError = IntegrityError
    session_maker: Callable[..., SessionProto] = field(init=False)
    _table_mapper: orm.registry = field(init=False)
    mappings: dict[Type[DomainModelBase], Table] = field(init=False, default_factory=dict)
    query: Any = field(init=False)
    aliased: aliased = field(init=False)
    desc: sa_desc = field(init=False)
    _mapping_started: bool = field(init=False, default=False)

    def __post_init__(self) -> None:
        self._engine = create_engine(self._db_url)
        self.session_maker = lambda: SQLAlchemySessionAdapter(sa_session_maker(bind=self._engine)())
        self._table_mapper = orm.registry()
        self.query = SQLAlchemyQueryAdapter
        self.aliased = aliased
        self.desc = sa_desc
        self._types_mapping = {
            int: Integer,
            Optional[int]: Integer,
            str: String,
            datetime: DateTime,
            Optional[datetime]: DateTime
        }
        self._values_mapping = {datetime.now: func.now()}

    def _init_table(self) -> None:
        """
        Initializes the mappings of domain models to SQLAlchemy tables.

        This method iterates over the domain models and creates SQLAlchemy table columns based on the model's
        annotated fields. It sets up each table with the appropriate columns and adds the table to the `mappings`
        dictionary.

        :raises StopIteration: If no primary key column is found while organizing columns.
        :raises domain_errors.DBError: If no mappings are provided after initialization.
        """
        for model in self._domain_models:
            columns = []
            for column_name, annotated_type in model.__annotations__.items():
                column_type, *kwargs_list = get_args(annotated_type)
                optional_params = {}
                for item in kwargs_list:
                    for key, value in item.items():
                        optional_params |= {key: self._values_mapping.get(value, value)}
                columns.append(Column(column_name, self._types_mapping[column_type], **(optional_params or {})))
                first_column = filter(lambda column: column.primary_key, columns)
                try:
                    columns = [columns.pop(columns.index(next(first_column))), *columns]
                except StopIteration:
                    pass
            self.mappings |= {
                model: Table(
                    model.__name__.lower(),
                    self._table_mapper.metadata,
                    *columns,
                    extend_existing=True
                )
            }

    def start_session(self) -> SQLAlchemySessionAdapter:
        session = self.session_maker()
        print(f"From start_session: {type(session) = }") # todo: remove
        return SQLAlchemySessionAdapter(session)

    def start_mapping(self) -> None:
        """
        Sets up the mappings of domain models to SQLAlchemy tables using imperative mapping in order to
        uncouple the domain models from the database.

        :raises domain_errors.DBError: If no mappings are provided after initialization.
        """
        if self._mapping_started:
            return
        self._init_table()
        print(f"From start_mapping: {self.mappings = }")  # todo: remove
        if not self.mappings:
            raise DBError(message="No mappings provided.")
        for model, table in self.mappings.items():
            self._table_mapper.map_imperatively(class_=model, local_table=table)
        self._mapping_started = True

    def create_tables(self) -> None:
        print("Creating tables...")  # todo: remove
        self._table_mapper.metadata.create_all(bind=self._engine)

    def drop_tables(self) -> None:
        print("Dropping tables...")  # todo: remove
        self._table_mapper.metadata.drop_all(bind=self._engine)
