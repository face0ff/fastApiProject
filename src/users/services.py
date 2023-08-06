"""Services module."""

from uuid import uuid4
from typing import Iterator

import loguru

from src.users.requests import UserRequest
from src.users.models import User


class UserService:

    def __init__(self, user_request: UserRequest) -> None:
        self.requests: UserRequest = user_request

    def get_users(self):
        return self.requests.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        return self.requests.get_by_id(user_id)

    def create_user(self, user_data) -> User:

        return self.requests.add(
            email=user_data.email,
            username=user_data.username,
            password=user_data.hashed_password,
            photo_path=user_data.photo_path,
        )
