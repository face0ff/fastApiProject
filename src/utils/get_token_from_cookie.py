import os

import jwt
from fastapi import HTTPException, status, Request


def get_token_from_cookie(request: Request):
    try:
        token = request.cookies.get("token")
        print(token)
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        email: str = payload.get("sub")
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
