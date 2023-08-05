from sqlalchemy import Column, String, Boolean, Integer

from src.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=True)
    username = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    photo_path = Column(String, nullable=True)
