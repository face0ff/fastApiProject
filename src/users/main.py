"""Application module."""
import uvicorn

from fastapi import FastAPI

from src.users.containers import Container
from src.users import endpoints



app = FastAPI()

# Include your routes here
app.include_router(endpoints.router)

@app.on_event("startup")
async def startup():
    container = Container()
    db = container.db()
    await db.create_database()

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='0.0.0.0', reload=True)