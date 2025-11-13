from pydantic import BaseModel
# from typing import Optional

class Auth(BaseModel):
    email: str
    password: str
    phone: str


class User(BaseModel):
    fullname: str
    email: str
    password: str
    phone: str


class BlogPost(BaseModel):
    title: str
    content: str
    comments: str

class BlogComment(BaseModel):
    comment: str
    blog_id: int
    user_id: int
