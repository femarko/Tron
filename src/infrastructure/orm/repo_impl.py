from typing import (
    Type,
)
from sqlalchemy import desc
from sqlalchemy.orm import aliased

from src.domain.models import (
    AddressBank,
    get_params,
)
from src.application.protocols import (
    SessionProto,
)


class AddressRepository:
    def __init__(
            self,
            session: SessionProto,
            model_cls: Type[AddressBank],

    ) -> None:
        self.session = session
        self.model_cls = model_cls

    def add(self, instance: AddressBank) -> None:
        self.session.add(instance)

    def get(self, instance_id: int) -> AddressBank:
        return self.session.get(model_cls=self.model_cls, instance_id=instance_id)

    def get_recent(self, number: int, page: int, per_page: int) -> dict[str, int | list[dict[str, str | int]]]:
        limited_subquery = (
            self.session.query(self.model_cls)
            .order_by(desc(self.model_cls.save_date))
            .limit(number)
            .subquery()
        )
        # limited_alias = aliased(self.model_cls, limited_subquery)  # todo: start fronm here
        offset: int = (page - 1) * per_page
        # total: int = limited_alias.count()
        total: int = limited_subquery.count()
        query_object = self.session.query(self.model_cls)
        model_instances: list[AddressBank] = query_object.offset(offset).limit(per_page).all()
        paginated_data: dict[str, int | list[dict[str, str | int]]] = {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "items": [get_params(model=model_instance) for model_instance in model_instances]
        }
        return paginated_data

    def delete(self, instance: AddressBank) -> None:
        self.session.delete(instance)


def create_address_repo(
        session: SessionProto,
        model_cls: Type[AddressBank] = AddressBank,
) -> AddressRepository:
    return AddressRepository(session=session, model_cls=model_cls)
