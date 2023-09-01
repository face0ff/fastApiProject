from sqlalchemy import Column, String, Boolean, Integer, DateTime, DECIMAL, ForeignKey, func
from sqlalchemy.orm import relationship
from src.database import Base
from src.ibay.models import Order


class Block(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True)

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True)
    balance = Column(DECIMAL, default=0)
    foto = Column(String, nullable=True)
    key = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="wallet")
    asset = relationship("Asset", back_populates="wallet")


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    decimal_places = Column(Integer, default=0)
    name = Column(String)
    image = Column(String, nullable=True)
    is_currency = Column(Boolean, default=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))

    wallet = relationship("Wallet", back_populates="asset")
    blockchain = relationship("Blockchain", back_populates="asset")


class Blockchain(Base):
    __tablename__ = "blockchains"

    id = Column(Integer, primary_key=True)
    network_id = Column(Integer)
    network_name = Column(String)
    rpc_url = Column(String)
    block_explorer_url = Column(String)
    symbol = Column(String)
    asset_id = Column(Integer, ForeignKey("assets.id"))

    asset = relationship("Asset", back_populates="blockchain")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    address_to = Column(String)
    address_from = Column(String)
    value = Column(DECIMAL)
    txn_hash = Column(String)
    status = Column(String, default='Pending')
    fee = Column(DECIMAL)
    age = Column(DateTime, default=func.now())

    order = relationship(Order, back_populates="transaction")



