"""Services module."""

from uuid import uuid4
from typing import Iterator

from src.users.requests import UserRequest
from src.users.models import User


class UserService:

    def __init__(self, user_request: UserRequest) -> None:
        self._requests: UserRequest = user_request

    def get_users(self) -> Iterator[User]:
        return self._requests.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        return self._requests.get_by_id(user_id)

    def create_user(self) -> User:
        uid = uuid4()
        return self._requests.add(email=f"{uid}@email.com", password="pwd", photo_path='123')
