import datetime
from decimal import Decimal

from gino import Gino
from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    DateTime,
    Numeric,
    Sequence,
    String,
    Boolean,
)

db = Gino()


class User(db.Model):
    __tablename__ = "users"
    idx: int = Column(BigInteger, primary_key=True)
    username: str = Column(String(255))
    first_name: str = Column(String(255), nullable=True)
    last_name: str = Column(String(255), nullable=True)

    is_active: bool = Column(Boolean, default=True)


class ServiceType(db.Model):
    __tablename__ = "service_types"
    idx: int = Column(BigInteger, Sequence("service_types_idx_seq"), primary_key=True)
    name: str = Column(String(255)) 

class Service(db.Model):
    __tablename__ = "services"
    idx: int = Column(BigInteger, Sequence("services_idx_seq"), primary_key=True)

    type: ServiceType = Column(ForeignKey("service_types.idx"))

    name: str = Column(String(255))
    description: str = Column(String(1024))
    amount: Decimal = Column(Numeric(12, 2))


class Payment(db.Model):
    __tablename__ = "payments"
    idx: int = Column(BigInteger, Sequence("payments_idx_seq"), primary_key=True)

    input_info: str = Column(String(2048))
    user: User = Column(ForeignKey("users.idx"))
    service: Service = Column(ForeignKey("services.idx"))

    date: datetime.datetime = Column(DateTime, default=datetime.datetime.now)


class SenderTemplate(db.Model):
    __tablename__ = "sender_templates"
    idx: int = Column(
        BigInteger, Sequence("sender_templates_idx_seq"), primary_key=True
    )

    photo: str = Column(String(2048))
    text: str = Column(String(2048))
    buttons: str = Column(String(2048))

    date: datetime.datetime = Column(DateTime, default=datetime.datetime.now)

class UserTemplate(db.Model):
    __tablename__ = "user_templates"
    idx: int = Column(
        BigInteger, Sequence("user_templates_idx_seq"), primary_key=True
    )

    name: str = Column(String(255), default=None, nullable=True)

    date: datetime = Column(DateTime, default=datetime.datetime.now)

class UserUserTemplateAssociation(db.Model):
    __tablename__ = "user_user_template_association"
    idx: int = Column(
        BigInteger, Sequence("user_user_template_association_idx_seq"), primary_key=True
    )
    
    user_template_id: int = Column(ForeignKey("user_templates.idx"))
    user_id: int = Column(ForeignKey("users.idx"))