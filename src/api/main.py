"""Application module."""
import uvicorn

from fastapi import FastAPI

import src
from src.api.containers import MainContainer

app = FastAPI()

# Include your routes here
app.include_router(src.users.endpoints.router)
app.include_router(src.wallet.endpoints.router)

container = MainContainer()


@app.on_event("startup")
async def startup():
    db = container.db()
    await db.create_database()


@app.on_event("shutdown")
async def shutdown():
    db = container.db()
    await db.close()


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='0.0.0.0', reload=True)
