# """Application module."""
# import uvicorn
#
# from fastapi import FastAPI
#
#
# from src.users.containers import UserContainer
# from src.users import endpoints
# from src.wallet import endpoints
#
# app = FastAPI()
#
# # Include your routes here
# # app.include_router(users.endpoints.router)
# # app.include_router(wallet.endpoints.router)
#
# container = UserContainer()
#
#
# @app.on_event("startup")
# async def startup():
#     db = container.db()
#     await db.create_database()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     db = container.db()
#     await db.disconnect()
#
#
# if __name__ == '__main__':
#     uvicorn.run("main:app", port=8000, host='0.0.0.0', reload=True)
