from pydantic import BaseModel


class Addr(BaseModel):
    addr: str
