from sqlalchemy import Column, String, Boolean, Integer, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
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


