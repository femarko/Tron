import src.orm_tool.sql_aclchemy_wrapper
from src.orm_tool.sql_aclchemy_wrapper import orm_conf

import src.domain.errors
from src.repository import AddressRepository, RepoProto


class UnitOfWork:
    def __init__(self):
        self.session_maker = orm_conf.session_maker

    def __enter__(self):
        self.session = self.session_maker()
        self.address_repo: RepoProto = AddressRepository(session=self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
            self.session.close()
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        try:
            self.session.commit()
        except orm_conf.integrity_error:
            raise src.domain.errors.AlreadyExistsError
