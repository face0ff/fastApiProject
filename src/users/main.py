"""Application module."""
import uvicorn

from fastapi import FastAPI

from src.users.containers import Container
from src.users import endpoints

app = FastAPI()

# Include your routes here
app.include_router(endpoints.router)

container = Container()


@app.on_event("startup")
async def startup():
    db = container.db()
    await db.create_database()


@app.on_event("shutdown")
async def shutdown():
    db = container.db()
    await db.disconnect()


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='0.0.0.0', reload=True)
