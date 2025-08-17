from src.application.protocols import ORMProto


class DBResetter:
    def __init__(self, orm: ORMProto) -> None:
        self.orm = orm

    def create_tables(self) -> None:
        self.orm.create_tables()

    def drop_tables(self) -> None:
        self.orm.drop_tables()

    def start_mapping(self) -> None:
        self.orm.start_mapping()