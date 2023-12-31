from pydantic import BaseModel, EmailStr, conint
from datetime import datetime




class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase): 
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    id: str | None = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)