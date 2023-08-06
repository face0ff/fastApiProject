"""Repositories module."""

from contextlib import AbstractContextManager
from fastapi import HTTPException, status
from typing import Callable, Iterator, ContextManager

from sqlalchemy.orm import Session

from src.users.models import User


class UserRequest:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self):
        with self.session_factory() as session:
            return session.query(User).all()

    def get_by_id(self, user_id: int):
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return user

    def add(self, email: str, username: str, photo_path: str, password: str, is_active: bool = True) -> User:
        with self.session_factory() as session:
            existing_user = session.query(User).filter(User.email == email).scalar()
            if existing_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already used")
            else:
                user = User(
                    email=email, username=username, hashed_password=password, is_active=is_active, photo_path=photo_path
                )
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
