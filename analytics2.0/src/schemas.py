import typing as t
import datetime
from pydantic import BaseModel
from decimal import Decimal
from src.database.models import TransactionType
from fastapi import Depends
from uuid import UUID

class ProxyCreate(BaseModel):
   host: str
   port: int
   username: str
   password: str
   scheme: str = "socks5"

class Proxy(ProxyCreate):
  id: int

class WorkerAmountUpdate(BaseModel):
   id: int
   amount: Decimal

class WorkerCreate(BaseModel):
   user: int
   proxy: int
   name: str

class Worker(WorkerCreate):
   amount: Decimal
   created_at: datetime.datetime

class TGUserCreate(BaseModel):
   id: int
   full_name: str
   username: t.Optional[str]
   worker_bot: UUID

class TGUserPatch(BaseModel):
   id: int
   worker_bot: UUID


class User(TGUserCreate):  
  last_activity: datetime.datetime
  first_touch: datetime.datetime
  is_active: bool

class TransitionCreate(BaseModel):
   worker_name: str

class Transition(TransitionCreate):
   id: int
   date: datetime.datetime

class MessageCreate(BaseModel):
  sender: int
  receiver: int
  text: t.Optional[str] = None
  photo: t.Optional[str] = None
  voice: t.Optional[str] = None

class MessageGet(BaseModel):
   sender: int
   receiver: int

class Message(MessageCreate):
   id: int
   date: datetime.datetime
   
class WorkerRequestCreate(BaseModel):
  bot_uid: UUID
  amount: Decimal
  is_admin: bool = False
  type: TransactionType

class WorkerRequest(WorkerRequestCreate):
   id: int
   date: datetime.datetime
   is_success: bool
   receipt: str
   comment: t.Optional[str]

class WorkerRequestPatch(BaseModel):
   id: int
   is_success: bool = False
   comment: t.Optional[str]


class AdminRequestCreate(BaseModel):
  amount: Decimal
  type: TransactionType

class AdminRequest(AdminRequestCreate):
   id: int
   date: datetime.datetime

class AdminPaymentDetailCreate(BaseModel):
  name: str
  text: str

class AdminPaymentDetail(AdminPaymentDetailCreate):
  id: int 

class UserPaymentDetailCreate(BaseModel):
  name: str
  user: int
  text: str

class UserPaymentDetail(AdminPaymentDetailCreate):
  id: int 


class AdminRequestCreate(BaseModel):
  amount: Decimal
  type: TransactionType

class WorkerRequest(WorkerRequestCreate):
   id: int
   date: datetime.datetime


class MatrixRequestCreate(BaseModel):
   user: int
   dob: str

class MatrixRequest(BaseModel):
   id: User
   worker_request: WorkerRequest
   user: User
   dob: t.Optional[str]
   image: t.Optional[str]
   result: t.Optional[str]


class BotCreate(BaseModel):
   name: str
   # main_description: str = "Описание"
   # service_description: str = "Чтобы узнать подробнее о каждом виде консультации, нажмите на соответствующую кнопку 👇"

class Bot(BotCreate):
   id: int
   uid:UUID