from typing import TypeVar
from sqlalchemy.orm.query import Query as SQLAlchemyQuery

from src.application.protocols import SessionProto


T = TypeVar("T")


class SQLAlchemyQueryAdapter:
    def __init__(self, sa_query: SQLAlchemyQuery):
        self._q = sa_query

    def filter_by(self, **kwargs):
        return SQLAlchemyQueryAdapter(self._q.filter_by(**kwargs))

    def order_by(self, *args):
        return SQLAlchemyQueryAdapter(self._q.order_by(*args))

    def limit(self, number):
        return SQLAlchemyQueryAdapter(self._q.limit(number))

    def offset(self, number):
        return SQLAlchemyQueryAdapter(self._q.offset(number))

    def first(self):
        return self._q.first()

    def all(self):
        return self._q.all()

    def count(self):
        return self._q.count()

    def subquery(self):
        return self._q.subquery()


class SQLAlchemySessionAdapter(SessionProto[T]):
    def __init__(self, sa_session):
        self._s = sa_session

    def add(self, instance):
        self._s.add(instance)

    def get(self, model_cls, instance_id):
        return self._s.get(model_cls, instance_id)

    def flush(self):
        self._s.flush()

    def delete(self, instance):
        self._s.delete(instance)

    def commit(self):
        self._s.commit()

    def rollback(self):
        self._s.rollback()

    def query(self, model_cls):
        return SQLAlchemyQueryAdapter(self._s.query(model_cls))

    def close(self):
        self._s.close()


class SQLAlchemySessionMakerAdapter:
    def __init__(self, sa_session_maker):
        self._sm = sa_session_maker

    def __call__(self) -> SQLAlchemySessionAdapter:
        return SQLAlchemySessionAdapter(self._sm())
