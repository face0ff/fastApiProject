"""Модуль для работы с репозиториями пользователей."""

from contextlib import AbstractContextManager
from fastapi import HTTPException, status
from typing import Callable, Iterator, ContextManager

from sqlalchemy.orm import Session

from src.users.models import User

from passlib.hash import bcrypt_sha256

class UserRequest:
    """
    Класс для работы с запросами, связанными с пользователями.
    """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        """
        Инициализация класса.

        :param session_factory: Функция для создания сессии SQLAlchemy.
        """
        self.session_factory = session_factory

    def get_all(self) -> Iterator[User]:
        """Получение всех пользователей."""
        with self.session_factory() as session:
            return session.query(User).all()

    def get_by_id(self, user_id: int) -> User:
        """
        Получение пользователя по его ID.

        :param user_id: ID пользователя.
        :return: Объект пользователя.
        """
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
            return user

    def get_by_email(self, email: str) -> User:
        """
        Получение пользователя по его электронной почте.

        :param email: Электронная почта пользователя.
        :return: Объект пользователя.
        """
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == email).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
            return user

    def add(self, user_data: User) -> User:
        """
        Добавление нового пользователя.

        :param user_data: Данные пользователя для добавления.
        :return: Объект нового пользователя.
        """
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == user_data.email).first()
            hashed_password = bcrypt_sha256.hash(user_data.password)
            if user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email уже используется")
            else:
                user = User(
                    email=user_data.email, username=user_data.username, hashed_password=hashed_password,
                    is_active=user_data.is_active, photo_path=user_data.photo_path
                )
                session.add(user)
                session.commit()
                session.refresh(user)
                return user

    def auth(self, auth_data: User) -> User:
        """
        Аутентификация пользователя.

        :param auth_data: Данные для аутентификации (почта и пароль).
        :return: Объект аутентифицированного пользователя.
        """
        with self.session_factory() as session:
            user = self.get_by_email(auth_data.email)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
            if bcrypt_sha256.verify(auth_data.password, user.hashed_password):
                return user
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не авторизован")
