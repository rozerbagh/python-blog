from sqlalchemy import Column, Integer, String
from db import Base
from pydantic import BaseModel
from typing import List, Optional

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "app"}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String)

class UserResponse(BaseModel):
    id: int
    fullname: str
    email: str
    phone: str

    class Config:
        orm_mode = True


class UserListResponse(BaseModel):
    message: str
    data: List[UserResponse]


class UserUpdateModel(BaseModel):
    fullname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None