import enum
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, ForeignKey, Integer, DateTime, Text, String, Numeric, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

_Base = declarative_base()


class Language(enum.Enum):
    RU = 'RU'
    ENG = 'ENG'


class BillType(enum.Enum):
    DEFAULT = 'DEFAULT'
    POSTPAID = 'POSTPAID'
    MIXED = 'MIXED'


class PaymentSource(enum.Enum):
    BACK_OFFICE = 'BACK_OFFICE'
    BANK = 'BANK'
    CASH = 'CASH'
    PAY_PAL = 'PAY_PAL'
    CRYPTO = 'CRYPTO'


class CartStatus(enum.Enum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    FAILED = "FAILED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"
    CANCELLED = "CANCELLED"
    REFUND = "REFUND"


@dataclass()
class Bill(_Base):
    __tablename__ = 'bill'

    id: int = Column(Integer, primary_key=True)
    creation_time: datetime = Column(DateTime, nullable=False)
    formulation: str = Column(Text, nullable=False)
    price: Decimal = Column(Numeric(10, 2), nullable=False)
    type: BillType = Column(Enum(BillType), nullable=False)
    payments = relationship('Payment', back_populates='bill')


@dataclass()
class Cart(_Base):
    __tablename__ = 'cart'

    id: int = Column(Integer, primary_key=True)
    creation_time: datetime = Column(DateTime, nullable=False)
    status: CartStatus = Column(Enum(CartStatus), nullable=False)
    price: Decimal = Column(Numeric(10, 2), nullable=False)
    description: str = Column(Text, nullable=False)
    shipping_address: str = Column(Text, nullable=False)
    bill_id: int = Column(Integer, ForeignKey('bill.id'), nullable=False)
    bill = relationship('Bill')
    customer_id: int = Column(Integer, ForeignKey('customer.id'), nullable=False)
    customer = relationship('Customer')
    purchases = relationship('Purchase', back_populates='cart')


@dataclass()
class Category(_Base):
    __tablename__ = 'category'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(60), nullable=False)


@dataclass()
class Customer(_Base):
    __tablename__ = 'customer'

    id: int = Column(Integer, primary_key=True)
    creation_time: datetime = Column(DateTime, nullable=False)
    first_name: str = Column(String(60), nullable=False)
    last_name: str = Column(String(60), nullable=False)
    middle_name: str = Column(String(60))
    lang: Language = Column(Enum(Language), nullable=False)
    email: str = Column(String(60), nullable=False)
    phone: str = Column(String(60), nullable=False)


@dataclass()
class Department(_Base):
    __tablename__ = 'department'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(60), nullable=False)
    category_id: int = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category')


@dataclass()
class Employee(_Base):
    __tablename__ = 'employee'

    id: int = Column(Integer, primary_key=True)
    first_name: str = Column(String(60), nullable=False)
    last_name: str = Column(String(60), nullable=False)
    middle_name: str = Column(String(60))
    department_id: int = Column(Integer, ForeignKey('department.id'), nullable=False)
    department = relationship(Department)


@dataclass()
class Payment(_Base):
    __tablename__ = 'payment'

    id: int = Column(Integer, primary_key=True)
    creation_time: datetime = Column(DateTime, nullable=False)
    amount: Decimal = Column(Numeric(10, 2), nullable=False)
    source: Language = Column(Enum(PaymentSource), nullable=False)
    bill_id: int = Column(Integer, ForeignKey('bill.id'), nullable=False)
    bill: Bill = relationship('Bill', back_populates='payments')


@dataclass()
class Product(_Base):
    __tablename__ = 'product'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(200), nullable=False)
    creation_time: datetime = Column(DateTime, nullable=False)
    price: Decimal = Column(Numeric(10, 2), nullable=False)
    category_id: int = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category')


@dataclass()
class Purchase(_Base):
    __tablename__ = 'purchase'

    creation_time: datetime = Column(DateTime, nullable=False)
    quantity: int = Column(Integer, nullable=False)
    cart_id: int = Column(Integer, ForeignKey('cart.id'), primary_key=True)
    cart = relationship('Cart', back_populates='purchases')
    product_id: int = Column(Integer, ForeignKey('product.id'), primary_key=True)
    product = relationship('Product')
