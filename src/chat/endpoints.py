# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from loguru import logger
# from fastapi import APIRouter
#
# from src.chat.services import ConnectionManager
#
# router = APIRouter(prefix="/chat", tags=['Chat'])
# manager = ConnectionManager()
#
#
# @router.get("/last_ten")
# async def get():
#     return True
#
#
# @router.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")
