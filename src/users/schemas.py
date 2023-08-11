import re
from pydantic import BaseModel, EmailStr, ValidationError, validator
from annotated_types import MaxLen, MinLen
from typing import Annotated


class User(BaseModel):
    id: int
    username: Annotated[str, MinLen(8), MaxLen(20)]
    email: EmailStr
    password1: str
    password2: str
    photo_path: str
    is_active: bool

    @validator("password1")
    def validate_password1_match(cls, value):
        if not value:
            return value

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,20}$", value):
            raise ValueError(
                "Password must contain at least one uppercase, one lowercase letter, one digit, and be between 8 and 20 characters")
        return value

    @validator("password2")
    def validate_password2_match(cls, value):
        if not value:
            return value
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,20}$", value):
            raise ValueError(
                "Password must contain at least one uppercase, one lowercase letter, one digit, and be between 8 and 20 characters")
        return value

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: EmailStr
    password: str
    button: bool

    class Config:
        from_attributes = True


class Profile(BaseModel):
    id: int
    username: str
    password1: str
    password2: str
    photo_path: str

    @validator("password1")
    def validate_password1_match(cls, value):
        if not value:
            return value

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,20}$", value):
            raise ValueError(
                "Password must contain at least one uppercase, one lowercase letter, one digit, and be between 8 and 20 characters")
        return value
    @validator("password2")
    def validate_password2_match(cls, value):
        if not value:
            return value
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,20}$", value):
            raise ValueError(
                "Password must contain at least one uppercase, one lowercase letter, one digit, and be between 8 and 20 characters")
        return value


    class Config:
        from_attributes = True

