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
