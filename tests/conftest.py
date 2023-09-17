import asyncio
from typing import AsyncGenerator

import pytest
from dependency_injector import providers, containers
from httpx import AsyncClient
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi import FastAPI
from propan.fastapi import RabbitRouter

from src import config_test_db
from src.chat.endpoints import router as chat_router
from src.database import Database
from src.ibay.endpoints import router as ibay_router
from src.users.repository import UserRequest
from src.users.services import UserService
from src.users.utils import send_registration_email
from src.wallet.endpoints import router as wallet_router
from src.users.endpoints import router as users_router


class MainTestContainer(containers.DeclarativeContainer):
    db = providers.Singleton(Database, db_url=config_test_db.db_url)

    user_request = providers.Factory(
        UserRequest,
        session_factory=db.provided.session,
        send_registration_email=send_registration_email,
    )

    user_service = providers.Factory(
        UserService,
        user_request=user_request,
    )


router = RabbitRouter('amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost')
app = FastAPI()
app.include_router(router)
app.include_router(users_router)
app.include_router(wallet_router)
app.include_router(ibay_router)
app.include_router(chat_router)
container = MainTestContainer()
db = container.db()


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    await db.create_database()
    await router.broker.start()

    yield app

    await db.delete_database()


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
