from fastapi import HTTPException, status, Response, Request
from fastapi import APIRouter, Depends
from contextlib import AbstractContextManager
from typing import Callable, Iterator
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.users.models import User
from src.wallet.models import Wallet, Transaction
from sqlalchemy import func


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

    async def get_all_user_wallets(self, email=None):

        user = await self.get_by_email(email)

        async with self.session_factory() as session:
            result = await session.execute(select(Wallet).where(Wallet.user_id == user.id))
            wallet_list = result.scalars().all()
            print(wallet_list)
            wallet_addresses = [wallet.address for wallet in wallet_list]
            return wallet_addresses

    async def get_all_wallets(self):

        async with self.session_factory() as session:
            result = await session.execute(select(Wallet))
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

    async def save_transaction(self, value, address_from, address_to, txn_hash=None, fee=None):

        from src.wallet.utils import create_transaction
        async with self.session_factory() as session:
            if txn_hash:
                await self.change_balance(address_from)
                await self.change_balance(address_to)
                result = await session.execute(select(Transaction).where(Transaction.txn_hash == txn_hash))
                transaction = result.scalars().first()
                if not transaction:
                    transaction = Transaction(address_from=address_from, address_to=address_to,
                                              txn_hash=txn_hash, status='Success', fee=fee,
                                              value=value)
                else:
                    transaction.status = "Success"
            else:
                try:
                    result = await session.execute(select(Wallet).where(Wallet.address == address_from))
                    wallet = result.scalars().first()
                    tx_data = await create_transaction(address_from, address_to, wallet.key, value)
                except:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Проверьте все что вы ввели")
                transaction = Transaction(address_from=address_from, address_to=address_to,
                                          txn_hash=tx_data['tx_hash'], status='Pending', fee=tx_data['fee'],
                                          value=tx_data['value'])
            session.add(transaction)
            await session.commit()
            await session.refresh(transaction)
            return transaction

    async def save_balance(self, address: str):
        balance = await self.get_balance(address)
        return balance

    async def change_balance(self, address: str):
        async with self.session_factory() as session:
            lowercase_address = address.lower()
            existing_wallet = await session.execute(
                select(Wallet).where(func.lower(Wallet.address) == lowercase_address))

            existing_wallet_instance = existing_wallet.scalar()
            if existing_wallet_instance:
                balance = await self.save_balance(address)
                existing_wallet_instance.balance = balance
                await session.commit()
                return balance
            else:
                return None

