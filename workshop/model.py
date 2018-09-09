import enum
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, ForeignKey, Integer, DateTime, Text, String, Numeric, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

_Base = declarative_base()


class CustomerLocale(enum.Enum):
    RU = 'RU'
    ENG = 'ENG'


@dataclass()
class Cart(_Base):
    __tablename__ = 'cart'

    cart_id: int = Column(Integer, primary_key=True)
    creation_time: datetime = Column(DateTime, nullable=False)
    customer_id: int = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    customer = relationship('Customer')
    price: Decimal = Column(Numeric(10, 2), nullable=False)
    purchases = relationship('Purchase')
    description: str = Column(Text, nullable=False)
    shipping_address: str = Column(Text, nullable=False)


@dataclass()
class Category(_Base):
    __tablename__ = 'category'

    category_id: int = Column(Integer, primary_key=True)
    name: str = Column(String(60), nullable=False)


@dataclass()
class Customer(_Base):
    __tablename__ = 'customer'

    customer_id: int = Column(Integer, primary_key=True)
    creation_time: datetime = Column(DateTime, nullable=False)
    first_name: str = Column(String(60), nullable=False)
    last_name: str = Column(String(60), nullable=False)
    middle_name: str = Column(String(60))
    locale: CustomerLocale = Column(Enum(CustomerLocale), nullable=False)
    email: str = Column(String(60), nullable=False)
    phone: str = Column(String(60), nullable=False)


@dataclass()
class Product(_Base):
    __tablename__ = 'product'

    product_id: int = Column(Integer, primary_key=True)
    name: str = Column(String(200), nullable=False)
    creation_time: datetime = Column(DateTime, nullable=False)
    category_id: int = Column(Integer, ForeignKey('category.category_id'), nullable=False)
    category = relationship('Category')
    price: Decimal = Column(Numeric(10, 2), nullable=False)
    short_description: str = Column(String(240), nullable=False)
    description: str = Column(Text, nullable=False)


@dataclass()
class Purchase(_Base):
    __tablename__ = 'purchase'

    creation_time: datetime = Column(DateTime, nullable=False)
    cart_id: int = Column(Integer, ForeignKey('cart.cart_id'), primary_key=True)
    product_id: int = Column(Integer, ForeignKey('product.product_id'), primary_key=True)
    product = relationship('Product')
    quantity: int = Column(Integer, nullable=False)
