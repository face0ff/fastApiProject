from pydantic import BaseModel, EmailStr
from annotated_types import MaxLen, MinLen
from typing import Annotated


class Product(BaseModel):
    id: int
    title: str
    price: float
    address: str
    img: str

    class Config:
        from_attributes = True


class Order(BaseModel):
    id: int
    address: str

    class Config:
        from_attributes = True
