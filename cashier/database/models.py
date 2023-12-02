from decimal import Decimal

from gino import Gino
from sqlalchemy import (BigInteger, Column, ForeignKey, Integer, Numeric,
                        Sequence, String, Boolean)

db = Gino()


class User(db.Model):
    __tablename__ = "users"
    idx: int = Column(BigInteger, primary_key=True)
    username: str = Column(String(255))

