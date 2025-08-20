from pydantic import BaseModel
from decimal import Decimal


class Addr(BaseModel):
    addr: str


class AddressInfoFromTron(BaseModel):
    id: int
    address: str
    balance: Decimal
    energy: int
    bandwidth: int


class EntriesFromDB(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    items: list[AddressInfoFromTron]


class FailedRequestToTron(BaseModel):
    address: str
    error: str


class FailedRequestToDB(BaseModel):
    error: str
