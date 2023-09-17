import asyncio
import logging

import loguru
import uvicorn

from fastapi import FastAPI
from propan.fastapi import RabbitRouter

import src
from src.api.containers import MainContainer
from src.api.consumer import main as listener_main

from src.chat.endpoints import router as chat_router
from src.database import Base
from src.ibay.endpoints import router as ibay_router
from src.wallet.endpoints import router as wallet_router
from src.users.endpoints import router as users_router
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)

router = RabbitRouter('amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost')

# app = FastAPI(lifespan=router.lifespan_context)
app = FastAPI()
# app.mount("/", app=sockets.app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Замените это на адрес вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include your routes here
app.include_router(router)
app.include_router(users_router)
app.include_router(wallet_router)
app.include_router(ibay_router)
app.include_router(chat_router)



@app.on_event("startup")
async def startup():

    container = MainContainer()
    db = container.db()
    await db.create_database()
    await router.broker.start()
    asyncio.create_task(listener_main())



@app.on_event("shutdown")
async def shutdown():
    await router.broker.stop()


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='127.0.0.1', reload=True)
