from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from src.users.models import Permission, User


class Permissions:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    async def get_chat_permission(self, email: str) -> bool:
        async with self.session_factory() as session:
            query = select(Permission).join(User).filter(User.email == email)
            result = await session.execute(query)
            permission = result.scalars().first()
            if not permission.has_chat_access:
                return False
            return True
