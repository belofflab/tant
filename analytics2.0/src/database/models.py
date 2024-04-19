import ormar
import datetime
import sqlalchemy
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4
from ormar.fields.constraints import UniqueColumns
from src.database.connection import database
from typing import ForwardRef

metadata = sqlalchemy.MetaData()


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


class TGUser(ormar.Model):
    class Meta(BaseMeta):
        tablename = "tgusers"

    id: int = ormar.BigInteger(primary_key=True)
    username: str = ormar.String(max_length=255, nullable=True)
    full_name: str = ormar.String(max_length=255)


# Главные модели аналитики
class Profile(ormar.Model):
    class Meta(BaseMeta):
        tablename = "profiles"

    id: int = ormar.BigInteger(primary_key=True)
    tguser = ormar.ForeignKey(TGUser, nullable=True)
    email: str = ormar.String(max_length=255, nullable=True, unique=True)
    access_token: str = ormar.String(max_length=2048, nullable=True)
    password: str = ormar.String(max_length=255, nullable=True)

    last_activity: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, index=True
    )
    first_touch: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, index=True
    )

    is_active: bool = ormar.Boolean(default=True)
    is_admin: bool = ormar.Boolean(default=False)


class ProfilePaymentDetail(ormar.Model):
    class Meta(BaseMeta):
        tablename = "profile_payment_details"

    id: int = ormar.Integer(primary_key=True)
    profile: Profile = ormar.ForeignKey(Profile, nullable=False)
    name: str = ormar.String(max_length=255, nullable=False)
    text: str = ormar.String(max_length=255, nullable=False)


class Bot(ormar.Model):
    class Meta(BaseMeta):
        tablename = "bots"

    id: int = ormar.BigInteger(primary_key=True)
    name: str = ormar.String(max_length=255)
    uid: UUID = ormar.UUID(default=uuid4, unique=True)
    total_users: int = ormar.Integer(minimum=0, default=0)
    amount: Decimal = ormar.Decimal(max_digits=12, decimal_places=2, default=0)
    freezed_amount: Decimal = ormar.Decimal(max_digits=12, decimal_places=2, default=0)
    comission: int = ormar.Integer(default=50, maximum=100, minimum=10)
    is_active = ormar.Boolean(default=True)


class BotProfile(ormar.Model):
    class Meta(BaseMeta):
        tablename = "bots_profiles"
        constraints = [UniqueColumns("bot", "profile")]

    id: int = ormar.BigInteger(primary_key=True)
    bot = ormar.ForeignKey(Bot, nullable=False)
    profile: Profile = ormar.ForeignKey(Profile, nullable=False)

    is_paid: bool = ormar.Boolean(default=False)
    created_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, index=True
    )
    next_payment: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, index=True
    )


class BotUser(ormar.Model):
    class Meta(BaseMeta):
        tablename = "bot_users"
        constraints = [UniqueColumns("bot", "tguser")]

    id: int = ormar.BigInteger(primary_key=True)
    bot = ormar.ForeignKey(Bot, nullable=False)
    tguser: TGUser = ormar.ForeignKey(TGUser, nullable=False)

    last_activity: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, index=True
    )
    first_touch: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now, index=True
    )

    is_active = ormar.Boolean(default=True)


class BotRequest(ormar.Model):
    class Meta(BaseMeta):
        tablename = "bot_requests"

    id: int = ormar.Integer(primary_key=True)
    bot: Bot = ormar.ForeignKey(Bot, nullable=False)
    amount: Decimal = ormar.Decimal(max_digits=20, decimal_places=2, default=0)
    marginal_amount: Decimal = ormar.Decimal(max_digits=20, decimal_places=2, default=0)
    worker_amount: Decimal = ormar.Decimal(max_digits=20, decimal_places=2, default=0)
    is_success: bool = ormar.Boolean(default=False)
    receipt: str = ormar.String(max_length=1024, nullable=True)
    comment: str = ormar.String(max_length=255, nullable=True, default=None)
    type: TransactionType = ormar.String(max_length=10, choices=TransactionType)
    date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, index=True)


# Услуги

CategoryRef = ForwardRef("Category")


class Category(ormar.Model):
    class Meta(BaseMeta):
        tablename = "taro_categories"

    id: int = ormar.BigInteger(primary_key=True)
    bot: Bot = ormar.ForeignKey(Bot, ondelete="CASCADE")
    name: str = ormar.String(max_length=255)
    photo: str = ormar.String(max_length=1024, nullable=True)
    parent = ormar.ForeignKey(CategoryRef, nullable=True)
    is_active = ormar.Boolean(default=True)


Category.update_forward_refs()


class Service(ormar.Model):
    class Meta(BaseMeta):
        tablename = "taro_services"

    id: int = ormar.BigInteger(primary_key=True)
    category: Category = ormar.ForeignKey(Category, nullable=True, ondelete="CASCADE")
    bot: Bot = ormar.ForeignKey(Bot)
    photo: str = ormar.String(max_length=1024, nullable=True)
    name: str = ormar.String(max_length=255)
    description: str = ormar.String(max_length=255)


class AdminPaymentDetail(ormar.Model):
    class Meta(BaseMeta):
        tablename = "admin_payment_details"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=255)
    text: str = ormar.String(max_length=255)


class AdminRequest(ormar.Model):
    class Meta(BaseMeta):
        tablename = "admin_requests"

    id: int = ormar.Integer(primary_key=True)
    amount: Decimal = ormar.Decimal(max_digits=12, decimal_places=2, default=0)
    type: TransactionType = ormar.String(max_length=10, choices=TransactionType)
    date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, index=True)


# class Message(ormar.Model):
#     class Meta(BaseMeta):
#         tablename = "messages"

#     id: int = ormar.Integer(primary_key=True)
#     sender: TGUser = ormar.ForeignKey(TGUser, related_name="sender")
#     receiver: TGUser = ormar.ForeignKey(TGUser, related_name="receiver")
#     text: str = ormar.String(max_length=2048, nullable=True)
#     photo: str = ormar.String(max_length=2048, nullable=True)
#     voice: str = ormar.String(max_length=2048, nullable=True)
#     date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, index=True)
