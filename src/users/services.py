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

    def create_user(self, user_data: dict) -> User:
        return self.requests.add(user_data)

    def auth_user(self, auth_data: dict, request, response) -> User:
        try:
            token = request.cookies.get("token")
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
            email: str = payload.get("sub")
            logger.info('email={}', email)
            jwt_token = self.create_jwt_token(auth_data)
            response.set_cookie(key="token", value=jwt_token)
            return self.requests.get_by_email(email)
        except jwt.PyJWTError:
            jwt_token = self.create_jwt_token(auth_data)
            return self.requests.auth(auth_data, response, jwt_token)

    def create_jwt_token(self, auth_data: dict):
        if not auth_data.button:
            time = timedelta(seconds=15)
            expiration = datetime.utcnow() + time
        else:
            expiration = datetime.utcnow() + timedelta(days=15)
        payload = {"sub": auth_data.email, "exp": expiration}
        jwt_token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm="HS256")
        return jwt_token
