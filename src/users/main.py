"""Application module."""
import uvicorn

from fastapi import FastAPI

from src.users.containers import Container
from src.users import endpoints


def create_app() -> FastAPI:
    container = Container()

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    return app


app = create_app()


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
