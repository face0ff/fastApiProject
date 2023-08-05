"""Repositories module."""

from contextlib import AbstractContextManager
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from .models import User


class UserRequest:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[User]:
        with self.session_factory() as session:
            return session.query(User).all()

    def get_by_id(self, user_id: int) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise FileNotFoundError
            return user

    def add(self, email: str, username: str, photo_path: str, password: str, is_active: bool = True) -> User:
        with self.session_factory() as session:
            user = User(email=email, username=username, hashed_password=password, is_active=is_active, photo_path=photo_path)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user