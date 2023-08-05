from pydantic import BaseModel, EmailStr
from annotated_types import MaxLen, MinLen
from typing import Annotated


class GetUser(BaseModel):
    id: int
    username: Annotated[str, MinLen(8), MaxLen(20)]
    email: EmailStr
    hashed_password: str
    photo_path: str

    class Config:
        orm_mode = True
