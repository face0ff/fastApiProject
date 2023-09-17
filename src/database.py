import logging
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import loguru
logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:

    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=True)
        self._session_factory = sessionmaker(
            self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def create_database(self) -> None:
        print("Davai po novoi Miha")
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        return True


    @asynccontextmanager
    async def session(self) -> AsyncSession:
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                logger.exception("Session rollback because of exception")
                await session.rollback()
                raise

    async def delete_database(self) -> None:
        print("Vse propalo")
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        return True
