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

    async def get_users(self):
        return await self.requests.get_all()

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.requests.get_by_id(user_id)

    async def create_user(self, user_data: dict) -> User:
        return await self.requests.add(user_data)

    async def auth_user(self, auth_data: dict, request, response) -> User:
        try:
            token = request.cookies.get("token")
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
            email: str = payload.get("sub")
            logger.info('email={}', email)
            jwt_token = await self.create_jwt_token(auth_data)
            response.set_cookie(key="token", value=jwt_token)
            return await self.requests.get_by_email(email)
        except jwt.PyJWTError:
            jwt_token = await self.create_jwt_token(auth_data)
            return await self.requests.auth(auth_data, response, jwt_token)

    async def create_jwt_token(self, auth_data: dict):
        if not auth_data.button:
            time = timedelta(seconds=15)
            expiration = datetime.utcnow() + time
        else:
            expiration = datetime.utcnow() + timedelta(days=15)
        payload = {"sub": auth_data.email, "exp": expiration}
        jwt_token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm="HS256")
        return jwt_token

    async def update_user(self, user_data: dict) -> User:
        return await self.requests.update(user_data)