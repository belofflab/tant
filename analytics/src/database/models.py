import typing as t
import ormar
import datetime
import sqlalchemy
from decimal import Decimal
from enum import Enum 

from src.database.connection import database

metadata = sqlalchemy.MetaData()


class TransactionType(str, Enum):
  DEPOSIT = "deposit"
  WITHDRAWAL = "withdrawal"

class BaseMeta(ormar.ModelMeta):
  database = database
  metadata = metadata

class Proxy(ormar.Model):
  class Meta(BaseMeta):
    tablename="proxies"
  
  id: int = ormar.BigInteger(primary_key=True)
  host: str = ormar.String(max_length=255)
  port: int = ormar.Integer()
  username: str = ormar.String(max_length=255)
  password: str = ormar.String(max_length=255)
  scheme: str = ormar.String(max_length=255)

class Worker(ormar.Model):
  class Meta(BaseMeta):
    tablename="workers"

  id: int = ormar.BigInteger(primary_key=True)
  username: str = ormar.String(max_length=255, nullable=True)
  name: str = ormar.String(max_length=255)
  amount: Decimal = ormar.Decimal(max_digits=12, decimal_places=2, default=0)
  freezed_amount: Decimal = ormar.Decimal(max_digits=12, decimal_places=2, default=0)
  comission: int = ormar.Integer(default=50)

  api_id: int = ormar.BigInteger()
  api_hash: str = ormar.String(max_length=1024)
  subdomain: str = ormar.String(max_length=255, nullable=True)
  hostname: str = ormar.String(max_length=255, default='belofflab.com', nullable=True)

  proxy: Proxy = ormar.ForeignKey(Proxy)
  is_active: bool = ormar.Boolean(default=True)
  created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)

class Transition(ormar.Model):
  class Meta(BaseMeta):
    tablename="transitions"

  id: int = ormar.BigInteger(primary_key=True)
  worker_name: str = ormar.String(max_length=255)
  date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)

class User(ormar.Model):
  class Meta(BaseMeta):
    tablename="users"
  
  id: int = ormar.BigInteger(primary_key=True)
  username: str = ormar.String(max_length=255, nullable=True)
  first_name: str = ormar.String(max_length=255, nullable=True)
  last_name: str = ormar.String(max_length=255, nullable=True)
  worker: Worker = ormar.ForeignKey(Worker)
  is_free_consulting: bool = ormar.Boolean(default=False)
  is_processing: bool = ormar.Boolean(default=False)
  last_activity: datetime.datetime = ormar.DateTime(default=datetime.datetime.now) 
  first_touch: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)

class Message(ormar.Model):
  class Meta(BaseMeta):
    tablename = "messages"
    
  id: int = ormar.Integer(primary_key=True)
  sender: User = ormar.ForeignKey(User, related_name="sender")
  receiver: User = ormar.ForeignKey(User, related_name="receiver")
  text: str = ormar.String(max_length=2048, nullable=True)
  photo: str = ormar.String(max_length=2048, nullable=True)
  voice: str = ormar.String(max_length=2048, nullable=True)
  date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)

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
  comment: str = ormar.String(max_length=255, defualt=None, nullable=True)
  type: TransactionType = ormar.String(max_length=10, choices=TransactionType)
  date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)

class MatrixUserRequest(ormar.Model):
  class Meta(BaseMeta):
    tablename="matrix_user_requests"
  id: int = ormar.Integer(primary_key=True)
  worker_request: WorkerRequest = ormar.ForeignKey(WorkerRequest)
  user: User = ormar.ForeignKey(User)
  dob: t.Optional[str] = ormar.String(max_length=60, nullable=True)
  image: t.Optional[str] = ormar.String(max_length=2048, nullable=True)
  result: t.Optional[str] = ormar.String(max_length=8096, nullable=True)

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
  date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)