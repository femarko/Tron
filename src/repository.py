from typing import Any, Protocol

from sqlalchemy import desc

from src.domain.models import AddressBank, get_params


class NotFoundError(Exception):
    pass


class RepoProto(Protocol):
    def add(self, instance) -> None:
        pass

    def get(self, instance_id: int) -> Any:
        pass

    def delete(self, instance) -> None:
        pass

    def get_recent(self, number, page, per_page) -> dict:
        pass


class Repository:
    def __init__(self, session):
        self.session = session
        self.model_cl = None

    def add(self, instance) -> None:
        self.session.add(instance)

    def get(self, instance_id: int) -> Any:
        return self.session.get(self.model_cl, instance_id)

    def get_recent(self, number: int, page: int, per_page: int) -> dict[str, int | list[dict[str, str | int]]]:
        query_object = self.session.query(self.model_cl).order_by(desc(self.model_cl.save_date)).limit(number)
        offset = (page - 1) * per_page
        total: int = query_object.count()
        model_instances: list = query_object.offset(offset).limit(per_page).all()
        paginated_data: dict[str, int | list[dict[str, str | int]]] = {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "items": [get_params(model=model_instance) for model_instance in model_instances]
        }
        return paginated_data

    def delete(self, instance) -> None:
        self.session.delete(instance)


class AddressRepository(Repository):
    def __init__(self, session):
        super().__init__(session=session)
        self.model_cl = AddressBank
