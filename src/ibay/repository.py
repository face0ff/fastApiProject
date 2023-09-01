"""Модуль для работы с репозиториями пользователей."""
from contextlib import AbstractContextManager
from fastapi import HTTPException, status, Response
from typing import Callable, Iterator
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from src.ibay.models import Product, Order
from src.users.models import User


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
                title=product_data.title, price=product_data.price, address=product_data.address,
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
