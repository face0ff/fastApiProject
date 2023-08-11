from fastapi import HTTPException, status, Response

from contextlib import AbstractContextManager
from typing import Callable, Iterator
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from src.users.models import User
from src.wallet.models import Wallet


class WalletRequest:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    async def get_by_email(self, email: str) -> User:
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
            return user

    async def save_wallet(self, wallet: int, key: str, user: User):
        async with self.session_factory() as session:
            existing_wallet = await session.execute(select(Wallet).where(Wallet.key == key))
            if existing_wallet.scalar():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Этот кошелек уже добавлен")
            wallet = Wallet(address=wallet.address, user_id=user.id, key=key)
            session.add(wallet)
            await session.commit()
            await session.refresh(wallet)
            return wallet
