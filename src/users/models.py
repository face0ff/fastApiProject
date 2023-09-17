from sqlalchemy import Column, String, Boolean, Integer, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from src.chat.models import Message
from src.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    photo_path = Column(String, nullable=True)

    wallet = relationship("Wallet", back_populates="user")
    order = relationship("Order", back_populates="user")
    permission = relationship('Permission', back_populates='user')
    message = relationship("Message", back_populates="user")


class Permission(Base):

    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    has_chat_access = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='permission')
