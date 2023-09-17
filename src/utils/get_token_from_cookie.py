import os

import jwt
from fastapi import HTTPException, status, Request


def get_email_from_cookie(request: Request):
    authorization_header = request.headers.get('authorization')
    if authorization_header:
        token = authorization_header.split(" ")[1]
    else:
        token = request.cookies.get("token")
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        email: str = payload.get("sub")
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")


def get_email_from_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        email: str = payload.get("sub")
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
