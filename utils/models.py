from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

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
    posts = relationship("Posts", back_populates="author")


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, unique=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    created_date = Column(Date)
    updated_date = Column(Date)
    title = Column(String)
    content = Column(String)

    # Fixed relationship
    reaction_love = relationship("Reactions", back_populates="post")


class Reactions(Base):
    __tablename__ = "reactions"
    id = Column(Integer, primary_key=True, unique=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer)

    # Added relationship back to Posts
    post = relationship("Posts", back_populates="reaction_love")

class PostsBase(BaseModel):
    title: str
    content: str

