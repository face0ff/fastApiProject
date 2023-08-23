import asyncio

import uvicorn

from fastapi import FastAPI
from propan.fastapi import RabbitRouter

import src
from src.api.containers import MainContainer
# from src.api.rabbit_utils import router

router = RabbitRouter('amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost')

app = FastAPI(lifespan=router.lifespan_context)

# Include your routes here
app.include_router(router)
app.include_router(src.users.endpoints.router)
app.include_router(src.wallet.endpoints.router)


@app.on_event("startup")
async def startup():
    container = MainContainer()
    db = container.db()
    await db.create_database()
    await router.broker.start()


@app.on_event("shutdown")
async def shutdown():
    await router.broker.stop()


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='127.0.0.1', reload=True)
