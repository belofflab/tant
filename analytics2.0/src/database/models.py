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


# Главные модели аналитики
class User(ormar.Model):
  class Meta(BaseMeta):
    tablename="users"
  
  id: int = ormar.BigInteger(primary_key=True)
  username: str = ormar.String(max_length=255, nullable=True)
  full_name: str = ormar.String(max_length=255)
  is_active: bool = ormar.Boolean(default=True)
  is_admin: bool = ormar.Boolean(default=False)
  password: str = ormar.String(max_length=255, default="password realiztion")
  last_activity: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, index=True) 
  first_touch: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, index=True)


class Proxy(ormar.Model):
  class Meta(BaseMeta):
    tablename="proxies"
  
  id: int = ormar.BigInteger(primary_key=True)
  host: str = ormar.String(max_length=255)
  port: int = ormar.Integer()
  username: str = ormar.String(max_length=255)
  password: str = ormar.String(max_length=255)
  scheme: str = ormar.String(max_length=15, default="socks5")


class Worker(ormar.Model):
  class Meta(BaseMeta):
    tablename="workers"
  id: int = ormar.BigInteger(primary_key=True)
  user: str = ormar.ForeignKey(User, unique=True)
  proxy: Proxy = ormar.ForeignKey(Proxy, unique=True)
  name: str = ormar.String(max_length=255)
  amount: Decimal = ormar.Decimal(max_digits=12, decimal_places=2, default=0)
  freezed_amount: Decimal = ormar.Decimal(max_digits=12, decimal_places=2, default=0)
  comission: int = ormar.Integer(default=50, maximum=100, minimum=10)
  is_active: bool = ormar.Boolean(default=True)

class WorkerConnection(ormar.Model):
  class Meta(BaseMeta):
    tablename="worker_connections"
  id: int = ormar.BigInteger(primary_key=True)
  worker: Worker = ormar.ForeignKey(Worker, unique=True)
  api_id: int = ormar.BigInteger()
  api_hash: str = ormar.String(max_length=1024)

class WorkerUser(ormar.Model):
  class Meta(BaseMeta):
    tablename="worker_users"
    constraints=[UniqueColumns("worker", "user")]
  id: int = ormar.BigInteger(primary_key=True)
  worker = ormar.ForeignKey(Worker)
  user: User = ormar.ForeignKey(User)

class Bot(ormar.Model):
  class Meta(BaseMeta):
    tablename="bots"

  id: int = ormar.BigInteger(primary_key=True)
  uid: UUID = ormar.UUID(default=uuid4, unique=True)
  main_photo: str = ormar.String(max_length=1024)
  main_description: str = ormar.String(max_length=200)
  service_photo: str = ormar.String(max_length=1024, nullable=True)
  service_description: str = ormar.String(max_length=255, default="Чтобы узнать подробнее о каждом виде консультации, нажмите на соответствующую кнопку 👇")
  free_consulting_photo: str = ormar.String(max_length=1024, nullable=True)
  free_consulting_description: str = ormar.String(max_length=200, default="Описание")

class BotWorker(ormar.Model):
  class Meta(BaseMeta):
    tablename="bot_workers"
    constraints=[UniqueColumns("bot", "worker")]
  id: int = ormar.BigInteger(primary_key=True)
  bot = ormar.ForeignKey(Bot)
  worker: Worker = ormar.ForeignKey(Worker)

class BotUser(ormar.Model):
  class Meta(BaseMeta):
    tablename="bot_users"
    constraints=[UniqueColumns("bot", "user")]
  id: int = ormar.BigInteger(primary_key=True)
  bot = ormar.ForeignKey(Bot)
  user: User = ormar.ForeignKey(User)
  last_activity: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, index=True) 
  first_touch: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, index=True)

# Услуги
  
CategoryRef = ForwardRef("Category")
class Category(ormar.Model):
  class Meta(BaseMeta):
    tablename="taro_categories"
  id: int = ormar.BigInteger(primary_key=True)
  bot: Bot = ormar.ForeignKey(Bot, ondelete="CASCADE")
  name: str = ormar.String(max_length=255)
  photo: str = ormar.String(max_length=1024, nullable=True)
  parent = ormar.ForeignKey(CategoryRef, nullable=True)
  is_active = ormar.Boolean(default=True)
Category.update_forward_refs()


class Service(ormar.Model):
  class Meta(BaseMeta):
    tablename="taro_services"
  id: int = ormar.BigInteger(primary_key=True)
  category: Category = ormar.ForeignKey(Category, nullable=True, ondelete="CASCADE")
  bot: Bot = ormar.ForeignKey(Bot)
  photo: str = ormar.String(max_length=1024, nullable=True, ondelete="CASCADE")
  name: str = ormar.String(max_length=255)
  description: str = ormar.String(max_length=255)


# Таро система
class Transition(ormar.Model):
  class Meta(BaseMeta):
    tablename="transitions"

  id: int = ormar.BigInteger(primary_key=True)
  worker_name: str = ormar.String(max_length=255)
  date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)


class Message(ormar.Model):
  class Meta(BaseMeta):
    tablename = "messages"
    
  id: int = ormar.Integer(primary_key=True)
  sender: User = ormar.ForeignKey(User, related_name="sender")
  receiver: User = ormar.ForeignKey(User, related_name="receiver")
  text: str = ormar.String(max_length=2048, nullable=True)
  photo: str = ormar.String(max_length=2048, nullable=True)
  voice: str = ormar.String(max_length=2048, nullable=True)
  date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, index=True)


class WorkerRequest(ormar.Model):
  class Meta(BaseMeta):
    tablename="worker_requests"

  id: int = ormar.Integer(primary_key=True)
  worker: Worker = ormar.ForeignKey(Worker)
  amount: Decimal = ormar.Decimal(max_digits=20, decimal_places=2, default=0)
  marginal_amount: Decimal = ormar.Decimal(max_digits=20, decimal_places=2, default=0)
  worker_amount: Decimal = ormar.Decimal(max_digits=20, decimal_places=2, default=0)
  is_success: bool = ormar.Boolean(default=0)
  receipt: str = ormar.String(max_length=1024, nullable=True)
  comment: str = ormar.String(max_length=255, default=None, nullable=True)
  type: TransactionType = ormar.String(max_length=10, choices=TransactionType)
  date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, index=True)


class UserPaymentDetail(ormar.Model):
  class Meta(BaseMeta):
    tablename="user_payment_details"
  id: int = ormar.Integer(primary_key=True)
  user: User = ormar.ForeignKey(User)
  name: str = ormar.String(max_length=255)
  text: str = ormar.String(max_length=255)

class AdminPaymentDetail(ormar.Model):
  class Meta(BaseMeta):
    tablename="admin_payment_details"
  id: int = ormar.Integer(primary_key=True)
  name: str = ormar.String(max_length=255)
  text: str = ormar.String(max_length=255)

class AdminRequest(ormar.Model):
  class Meta(BaseMeta):
    tablename="admin_requests"

  id: int = ormar.Integer(primary_key=True)
  amount: Decimal = ormar.Decimal(max_digits=12, decimal_places=2, default=0)
  type: TransactionType = ormar.String(max_length=10, choices=TransactionType)
  date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now, index=True)

# class MatrixUserRequest(ormar.Model):
#   class Meta(BaseMeta):
#     tablename="matrix_user_requests"
#   id: int = ormar.Integer(primary_key=True)
#   worker_request: WorkerRequest = ormar.ForeignKey(WorkerRequest)
#   user: User = ormar.ForeignKey(User)
#   dob: t.Optional[str] = ormar.String(max_length=60, nullable=True)
#   image: t.Optional[str] = ormar.String(max_length=2048, nullable=True)
#   result: t.Optional[str] = ormar.String(max_length=8096, nullable=True)