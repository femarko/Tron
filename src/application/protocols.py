from typing import Protocol, Any


class RepoProto(Protocol):
    def add(self, instance) -> None:
        pass

    def get(self, instance_id: int) -> Any:
        pass

    def delete(self, instance) -> None:
        pass

    def get_recent(self, number, page, per_page) -> dict:
        pass
