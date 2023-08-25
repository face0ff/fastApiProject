"""Модуль для работы с репозиториями пользователей."""
import asyncio
from contextlib import AbstractContextManager
from redis.asyncio.client import Redis
import loguru
from fastapi import HTTPException, status, Response
from typing import Callable, Iterator
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.users.models import User

from passlib.hash import bcrypt_sha256


class UserRequest:
    """
    Класс для работы с запросами, связанными с пользователями.
    """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]],
                 send_registration_email) -> None:
        """
        Инициализация класса.

        :param session_factory: Функция для создания сессии SQLAlchemy.
        """
        self.session_factory = session_factory
        self.send_registration_email = send_registration_email

    async def get_all(self) -> Iterator[User]:
        """Получение всех пользователей."""
        async with self.session_factory() as session:
            result = await session.execute(select(User))
            return result.scalars().all()

    async def get_by_id(self, user_id: int) -> User:
        """
        Получение пользователя по его ID.

        :param user_id: ID пользователя.
        :return: Объект пользователя.
        """
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
            return user

    async def get_by_email(self, email: str) -> User:
        """
        Получение пользователя по его электронной почте.

        :param email: Электронная почта пользователя.
        :return: Объект пользователя.
        """
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
            async with Redis.from_url("redis://localhost") as redis:
                await redis.set('id', user.id)
            return user

    async def add(self, user_data: dict) -> User:

        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.email == user_data.email))
            user = result.scalar()
            hashed_password = bcrypt_sha256.hash(user_data.password)
            if user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email уже используется")
            else:
                # from src.users.utils import send_registration_email
                user = User(
                    email=user_data.email, username=user_data.username, hashed_password=hashed_password,
                    is_active=user_data.is_active, photo_path=user_data.photo_path
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                loop = asyncio.get_running_loop()
                loop.run_in_executor(None, self.send_registration_email,user_data.email, user_data.username)
                return user

    async def auth(self, auth_data: dict, response: Response, jwt_token) -> User:
        async with self.session_factory() as session:
            user = await self.get_by_email(auth_data.email)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
            if bcrypt_sha256.verify(auth_data.password, user.hashed_password):
                response.set_cookie(key="token", value=jwt_token)
                return user
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неправильный пароль")


    async def update(self, user_data: dict, email) -> User:
        hashed_password = bcrypt_sha256.hash(user_data.password1)
        async with self.session_factory() as session:
            user = await self.get_by_email(email)
            user.hashed_password = hashed_password if user_data.password1 else user.hashed_password
            user.username = user_data.username if user_data.username else user.username
            user.photo_path = user_data.photo_path if user_data.photo_path else user.photo_path
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user


