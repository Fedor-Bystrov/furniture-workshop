import enum
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, Integer, DateTime, Text, Numeric, Enum
from sqlalchemy.ext.declarative import declarative_base

_Base = declarative_base()


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
