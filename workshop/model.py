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


@dataclass()
class Bill(_Base):
    __tablename__ = 'bill'

    id: int = Column(Integer, primary_key=True)
    creation_time: datetime = Column(DateTime, nullable=False)
    formulation: str = Column(Text, nullable=False)
    price: Decimal = Column(Numeric(10, 2), nullable=False)
    type: BillType = Column(Enum(BillType), nullable=False)


class Cart:
    pass


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
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category: Category = relationship("Category")


class Employee:
    pass


class Payment:
    pass


class Product:
    pass


class Purchase:
    pass
