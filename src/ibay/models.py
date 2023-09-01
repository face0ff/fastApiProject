from sqlalchemy import Column, String, Boolean, Integer, DateTime, DECIMAL, ForeignKey, func
from sqlalchemy.orm import relationship
from src.database import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(DECIMAL, default=0)
    address = Column(String)
    img = Column(String, nullable=True)

    order = relationship("Order", back_populates="product")


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    status = Column(String, default='New')
    date = Column(DateTime, default=func.now())
    refund = Column(Boolean, default=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="order")
    product = relationship("Product", back_populates="order")
    transaction = relationship("Transaction", back_populates="order")
