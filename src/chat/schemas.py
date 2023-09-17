import re
from pydantic import BaseModel, EmailStr, ValidationError, validator
from annotated_types import MaxLen, MinLen
from typing import Annotated


class Message(BaseModel):
    message: str
    img: str


    class Config:
        from_attributes = True


