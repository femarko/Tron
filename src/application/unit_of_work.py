from typing import (
    Type,
    Callable
)

from src.domain.models import DomainModel
from src.domain.errors import (
    AlreadyExistsError,
    RepoError
)
from src.application.protocols import (
    AddressBankRepoProto,
    SessionProto,
    UoWProto,
    ORMProto
)


class UnitOfWork:
    def __init__(
            self,
            orm_tool: ORMProto,
            model_cls: Type[DomainModel],
            repo_creators: dict[Type[DomainModel], Callable[[SessionProto, Type[DomainModel]], AddressBankRepoProto]]
    ):
        self.orm = orm_tool
        self.model_cls = model_cls
        self.repo_creators = repo_creators
        self._repo = None

    def __enter__(self) -> "UoWProto":
        self.session: SessionProto = self.orm.start_session()
        repo_creator = self.repo_creators.get(self.model_cls)
        self._repo = repo_creator(self.session, self.model_cls)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.rollback()
            self.session.close()
        self.session.close()

    def commit(self) -> None:
        try:
            self.session.commit()
        except self.orm.integrity_error:
            raise AlreadyExistsError

    def flush(self) -> None:
        try:
            self.session.flush()
        except self.orm.integrity_error:
            raise AlreadyExistsError

    def rollback(self) -> None:
        self.session.rollback()

    @property
    def repo(self) -> AddressBankRepoProto:
        if self._repo is None:
            raise RepoError(message="Repo is not initialized.")
        return self._repo
