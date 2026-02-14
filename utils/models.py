from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from utils.database import Base

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class LoginBase(BaseModel):
    email:str
    password:str
  
class User(Base):
    __tablename__ = "users"
    id = Column[int](Integer, primary_key=True, index=True)
    name = Column[str](String, index=True)
    email = Column[str](String, unique=True, index=True)
    hashed = Column[str](String, unique=True, index=False)
