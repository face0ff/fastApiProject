from sqlalchemy.orm import joinedload
from contextlib import AbstractContextManager
from typing import Callable, Iterator
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import desc
from src.chat.models import Message
from src.users.models import User


class ChatRequest:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    async def get_last_ten_messages_from_base(self):
        async with self.session_factory() as session:
            query = (
                select(Message)
                .join(User)
                .options(joinedload(Message.user))
                .order_by(desc(Message.date))
                .limit(10)
            )
            result = await session.execute(query)
            last_ten_messages = result.scalars().all()
            last_ten_messages.reverse()
            return last_ten_messages


    async def save_last_message_from_base(self, data: dict, email):
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            message = Message(
                message=data.message,
                img=data.img,
                user_id=user.id
            )
            session.add(message)
            await session.commit()
            await session.refresh(message)
            return message
