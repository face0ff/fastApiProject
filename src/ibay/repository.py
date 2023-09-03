"""Модуль для работы с репозиториями пользователей."""
from contextlib import AbstractContextManager

import loguru
from fastapi import HTTPException, status, Response
from typing import Callable, Iterator
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from src.ibay.models import Product, Order
from src.users.models import User
from src.wallet.containers import WalletContainer
from src.wallet.models import Transaction


class ProductRequest:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    async def get_all(self) -> Iterator[Product]:
        """Получение всех пользователей."""
        async with self.session_factory() as session:
            result = await session.execute(select(Product))
            return result.scalars().all()

    async def get_by_id(self, product_id: int) -> User:
        async with self.session_factory() as session:
            result = await session.execute(select(Product).where(Product.id == product_id))
            product = result.scalars().first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден")
            return product

    async def add(self, product_data: dict) -> Product:
        async with self.session_factory() as session:
            product = Product(
                title=product_data.title,
                price=product_data.price,
                address=product_data.address,
                img=product_data.img
            )
            session.add(product)
            await session.commit()
            await session.refresh(product)
            return product


class OrderRequest:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    async def get_all(self, email) -> Iterator[Order]:
        print(email)
        """Получение всех ордеров."""
        async with self.session_factory() as session:
            query = select(Order).join(User).filter(User.email == email)
            result = await session.execute(query)
            return result.scalars().all()

    async def add(self, order_data: dict, email) -> Order:
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            result = await session.execute(select(Product).where(Product.id == order_data.product_id))
            product = result.scalars().first()

            service = WalletContainer.wallet_service()
            transaction = await service.create_transaction(product.price, order_data.address, product.address)

            order = Order(
                product_id=order_data.product_id,
                user_id=user.id,
                transaction_id=transaction.id
            )
            session.add(order)
            await session.commit()
            await session.refresh(order)
            return order

    async def change_status(self, body) -> Order:
        async with self.session_factory() as session:
            query = select(Order).filter(Order.transaction_id == body['transaction_id'])
            result = await session.execute(query)
            order = result.scalars().first()
            order.status = body['result']
            if body['result'] == 'Failed':
                await self.refund(body['transaction_id'])
            await session.commit()

    async def refund(self, transaction_id) -> Order:
        loguru.logger.critical("REFUNDREFUNDREFUNDREFUNDREFUNDREFUNDREFUNDREFUNDREFUNDREFUNDREFUND")
        async with self.session_factory() as session:
            query = select(Order).filter(Order.transaction_id == transaction_id)
            result = await session.execute(query)
            refund_order = result.scalars().first()

            query = select(Transaction).filter(Transaction.id == transaction_id)
            result = await session.execute(query)
            refund_transaction = result.scalars().first()



            service = WalletContainer.wallet_service()
            transaction = await service.create_transaction(
                float(refund_transaction.value) + float(refund_transaction.fee) * 1.5,
                refund_transaction.address_to,
                refund_transaction.address_from)

            refund_order.transaction_id = transaction.id
            refund_order.refund = True
            session.add(refund_order)
            await session.commit()
            await session.refresh(refund_order)
            return refund_order
