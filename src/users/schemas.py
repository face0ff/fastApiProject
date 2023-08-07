import re
from pydantic import BaseModel, EmailStr, ValidationError, validator
from annotated_types import MaxLen, MinLen
from typing import Annotated



class User(BaseModel):
    id: int
    username: Annotated[str, MinLen(8), MaxLen(20)]
    email: EmailStr
    password: str
    photo_path: str
    is_active: bool

    @validator("password")
    def validate_password_complexity(cls, value):
        # Проверка сложности пароля: минимум 1 символ, 1 ловеркейс, 1 апперкейс, 1 цифра, 8-20 символов
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