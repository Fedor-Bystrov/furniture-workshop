from dataclasses import dataclass

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

_Base = declarative_base()


@dataclass()
class Category(_Base):
    __tablename__ = 'category'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(60), nullable=False)
