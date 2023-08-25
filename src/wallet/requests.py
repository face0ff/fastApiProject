
from fastapi import HTTPException, status, Response, Request
from fastapi import APIRouter, Depends
from contextlib import AbstractContextManager
from typing import Callable, Iterator
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.users.models import User
from src.wallet.models import Wallet, Transaction



class WalletRequest:

    def __init__(self, get_balance, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory
        self.get_balance = get_balance
    async def get_by_id(self, user_id: int) -> User:
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
            return user

    async def get_by_email(self, email: str) -> User:
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
            return user

    async def get_all_wallets(self, email=None, id=None):

        if email:
            user = await self.get_by_email(email)
        else:
            user = await self.get_by_id(id)
        async with self.session_factory() as session:
            result = await session.execute(select(Wallet).where(Wallet.user_id == user.id))
            wallet_list = result.scalars().all()
            print(wallet_list)
            wallet_addresses = [wallet.address for wallet in wallet_list]
            return wallet_addresses

    async def save_wallet(self, wallet: int, key: str, user: User):
        async with self.session_factory() as session:
            existing_wallet = await session.execute(select(Wallet).where(Wallet.key == key))
            balance = await self.save_balance(wallet.address)
            if existing_wallet.scalar():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Этот кошелек уже добавлен")
            wallet = Wallet(address=wallet.address, user_id=user.id, key=key, balance=balance)
            session.add(wallet)
            await session.commit()
            await session.refresh(wallet)
            return wallet

    async def save_transaction(self, value, wallet_sender, wallet_receiver):
        from src.wallet.utils import create_transaction
        async with self.session_factory() as session:
            try:
                result = await session.execute(select(Wallet).where(Wallet.address == wallet_sender))
                wallet = result.scalars().first()
                tx_data = await create_transaction(wallet_sender, wallet_receiver, wallet.key, value)
            except:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Проверьте все что вы ввели")
            print('111111111111111111111111111110', type(value), type(tx_data['fee']))
            transaction = Transaction(address_from=wallet_sender, address_to=wallet_receiver,
                                      txn_hash=tx_data['tx_hash'], status='Pending', fee=tx_data['fee'],
                                      value=tx_data['value'])
            session.add(transaction)
            await session.commit()
            await session.refresh(transaction)
            return transaction

    async def save_balance(self, address: str):
        balance = await self.get_balance(address)
        return balance