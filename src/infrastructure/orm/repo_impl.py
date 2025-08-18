from typing import (
    Type,
    Optional
)
from decimal import Decimal

from src.domain.models import (
    AddressBank,
    get_params,
)
from src.domain.errors import (
    AlreadyExistsError,
    DBError
)
from src.application.protocols import (
    SessionProto,
    ORMProto
)


class AddressRepository:
    def __init__(
            self,
            orm: ORMProto,
            session: SessionProto,
            model_cls: Type[AddressBank]
    ) -> None:
        self.session = session
        self.orm = orm
        self.model_cls = model_cls

    def add(self, instance: AddressBank) -> None:
        try:
            self.session.add(instance)
        except self.orm.integrity_error as e:
            raise AlreadyExistsError from e
        except self.orm.sqlalchemy_error as e:
            raise DBError from e

    def get(self, instance_id: int) -> Optional[AddressBank]:
        try:
            return self.session.get(model_cls=self.model_cls, instance_id=instance_id)
        except self.orm.sqlalchemy_error as e:
            raise DBError from e

    def get_recent(
            self,
            limit_total: int,
            page: int,
            per_page: int
    ) -> dict[str, int | list[dict[str, str | int | Decimal]]]:
        try:
            limited_subquery = (
                self.session.query(self.model_cls)
                .order_by(self.orm.desc(self.model_cls.save_date))
                .limit(limit_total)
                .subquery()
            )
        except self.orm.sqlalchemy_error as e:
            raise DBError from e
        offset: int = (page - 1) * per_page
        try:
            query_object = self.session.query(limited_subquery)
        except self.orm.sqlalchemy_error as e:
            raise DBError from e
        total: int = query_object.count()
        model_instances: list[AddressBank] = query_object.offset(offset).limit(per_page).all()
        paginated_data: dict[str, int | list[dict[str, str | int | Decimal]]] = {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "items": [get_params(model=model_instance) for model_instance in model_instances]
        }
        return paginated_data

    def delete(self, instance: AddressBank) -> None:
        try:
            self.session.delete(instance)
        except self.orm.sqlalchemy_error as e:
            raise DBError from e

def create_address_repo(
        session: SessionProto,
        orm: ORMProto,
        model_cls: Type[AddressBank] = AddressBank,
) -> AddressRepository:
    return AddressRepository(session=session, orm=orm, model_cls=model_cls)
