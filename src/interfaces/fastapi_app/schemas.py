from pydantic import BaseModel
from decimal import Decimal


class Addr(BaseModel):
    addr: str


class AddressInfo(BaseModel):
    id: int
    address: str
    balance: Decimal
    energy: int
    bandwidth: int


class FailedRequest(BaseModel):
    address: str
    error: str
