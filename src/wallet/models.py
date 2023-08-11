from sqlalchemy import Column, String, Boolean, Integer, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class Wallet(Base):

    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=True)
    balance = Column(DECIMAL, nullable=True)
    foto = Column(String, nullable=True)
    key = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="wallet")
    asset = relationship("Asset", back_populates="wallet")


class Asset(Base):

    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    decimal_places = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    image = Column(String, nullable=True)
    is_currency = Column(Boolean, default=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))

    wallet = relationship("Wallet", back_populates="asset")
