from src.database import Base
from sqlalchemy import Column, String, Boolean, Integer, DateTime, DECIMAL, ForeignKey, func
from sqlalchemy.orm import relationship


class Message(Base):

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    message = Column(String)
    img = Column(String, nullable=True)
    date = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="message")
