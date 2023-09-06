from fastapi import HTTPException, status
from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from src.ibay.models import Order
from src.users.models import User
from src.wallet.config_wallet import router
from src.wallet.models import Wallet, Transaction, Block
from sqlalchemy import func
import loguru


class WalletRequest:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

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

    async def get_all_user_transactions(self, email):

        user = await self.get_by_email(email)

        async with self.session_factory() as session:
            query = select(Transaction).join(Wallet, ((Transaction.address_from == Wallet.address) | (
                    Transaction.address_to == Wallet.address))).filter(Wallet.user_id == user.id)
            transactions_list = await session.execute(query)
            transactions_list = transactions_list.scalars().all()

            loguru.logger.info(f"Transactions for user {email}: {transactions_list}")

            return transactions_list

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

        from src.wallet.wallet_utils.transaction_create import create_transaction
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
                    result = await session.execute(select(Order).where(Order.transaction_id == transaction.id))
                    order = result.scalars().first()
                    if order:
                        if not order.refund:
                            async with router.broker as broker:
                                body = {
                                    'result': "Success",
                                    'transaction_id': transaction.id
                                }
                                await broker.publish(body, queue="transaction_success")
                        else:
                            async with router.broker as broker:
                                body = {
                                    'result': "Refund",
                                    'transaction_id': transaction.id
                                }
                                await broker.publish(body, queue="transaction_success")

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
        from src.wallet.wallet_utils.wallet_balance import get_balance
        balance = await get_balance(address)
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

    async def last_block_save(self, block_number: int):
        async with self.session_factory() as session:
            result = await session.execute(select(Block))
            last_block = result.scalar()
            if last_block:
                last_block.number = block_number
            else:
                last_block = Block(number=block_number)
                session.add(last_block)

            await session.commit()

    async def get_last_block_from_base(self):
        async with self.session_factory() as session:
            result = await session.execute(select(Block))
            last_block = result.scalar()
            return last_block.number
