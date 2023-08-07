"""Services module."""
import os
from datetime import timedelta, datetime

from fastapi import HTTPException, status

import jwt
from loguru import logger

from src.users.requests import UserRequest
from src.users.models import User



class UserService:

    def __init__(self, user_request: UserRequest) -> None:
        self.requests: UserRequest = user_request

    def get_users(self):
        return self.requests.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        return self.requests.get_by_id(user_id)

    def create_user(self, user_data: dict, response) -> User:
        jwt_token = self.create_jwt_token(user_data, button=True)
        logger.info("token = {}", jwt_token)
        response.set_cookie(key="token", value=jwt_token)
        return self.requests.add(user_data)

    def auth_user(self, auth_data: dict) -> User:
        # try:
        #
        #     payload = jwt.decode(response.token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        #     email: str = payload.get("sub")
        #     logger.info('email={}', email)
        #     return self.requests.get_by_email(email)
        # except jwt.PyJWTError:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен")

        return self.requests.auth(auth_data)

    def create_jwt_token(self, user_data: dict, button):
        if not button:
            time = timedelta(seconds=15)
            expiration = datetime.utcnow() + time
        else:
            expiration = datetime.utcnow() + timedelta(days=15)
        payload = {"sub": user_data.email, "exp": expiration}
        jwt_token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm="HS256")
        return jwt_token
