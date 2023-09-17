from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from loguru import logger
from fastapi import APIRouter, Depends, Response
from fastapi.responses import FileResponse
from dependency_injector.wiring import inject, Provide

from src.chat import schemas
from src.chat.containers import ChatContainer
from src.chat.repository import ChatRequest
from src.chat.services import ConnectionManager
from src.users.containers import UserContainer
from src.utils.get_token_from_cookie import get_email_from_cookie, get_email_from_token

router = APIRouter(prefix="/chat", tags=['Chat'])
manager = ConnectionManager()


@router.get("/")
async def get(email: str = Depends(get_email_from_cookie)):
    print(email)
    return FileResponse(path='templates/chat.html')


@router.get("/get_last_ten_messages/")
@inject
async def get_last_ten(
        chat_request: ChatRequest = Depends(Provide[ChatContainer.chat_request])):
    return await chat_request.get_last_ten_messages_from_base()


@router.post("/save_last_message/")
@inject
async def get_last_message(
        data: schemas.Message,
        email: str = Depends(get_email_from_cookie),
        chat_request: ChatRequest = Depends(Provide[ChatContainer.chat_request])):
    return await chat_request.save_last_message_from_base(data, email)



@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, email: str = Depends(get_email_from_token)):
    request = UserContainer.user_request()
    user = await request.get_by_email(email)
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client name >>{user.username} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client name >>{user.username} left the chat")


