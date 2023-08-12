import httpx
from fastapi import HTTPException, status, Response

from contextlib import AbstractContextManager
from typing import Callable, Iterator
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from src.users.models import User
from src.wallet.config_wallet import api_etherscan_url, api_etherscan
from src.wallet.models import Wallet, Transaction



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
            balance = await self.save_balance(wallet.address)
            print(balance)
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
            result = await session.execute(select(Wallet).where(Wallet.address == wallet_sender))
            wallet = result.scalars().first()
            try:
                tx_data = await create_transaction(wallet_sender, wallet_receiver, wallet.key, value)
            except:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Проверьте все что вы ввели")

            transaction = Transaction(address_from=wallet_sender, address_to=wallet_receiver, txn_hash=tx_data['tx_hash'], status='Pending', fee=tx_data['fee'], value=value)
            session.add(transaction)
            await session.commit()
            await session.refresh(transaction)
            return transaction

    async def save_balance(self, address: str):
        headers = {
            "accept": "application/json",
        }
        params = {

            "action": "balancemulti",
            "address": address,
            "tag": "latest",
            "apikey": api_etherscan
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{api_etherscan_url}?module=account",
                headers=headers,
                params=params,
            )
            if response.status_code == 200:
                result = response.json()
                print(result['result'])
                return result['result'][0]['balance']
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Проверьте все что вы ввели")
