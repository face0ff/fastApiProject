from sqlalchemy import Column, String, Boolean, Integer, DateTime, DECIMAL, ForeignKey, func
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
    blockchain = relationship("Blockchain", back_populates="asset")


class Blockchain(Base):

    __tablename__ = "blockchains"

    id = Column(Integer, primary_key=True)
    network_id = Column(Integer, nullable=True)
    network_name = Column(String, nullable=True)
    rpc_url = Column(String, nullable=True)
    block_explorer_url = Column(String, nullable=True)
    symbol = Column(String, nullable=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))

    asset = relationship("Asset", back_populates="blockchain")



class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    address_to = Column(String, nullable=True)
    address_from = Column(String, nullable=True)
    value = Column(DECIMAL, nullable=True)
    txn_hash = Column(String, nullable=True)
    status = Column(String, nullable=True)
    fee = Column(DECIMAL, nullable=True)
    age = Column(DateTime, default=func.now())



