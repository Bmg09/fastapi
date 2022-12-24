from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime
from pydantic.types import conint
class userResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True
class PostModel(BaseModel):
    title: str
    content: str 
    published : bool = True #default value is True if not provided in the request body optional field

class PostCreate(PostModel):
    pass

class Post(PostModel):
    id : int
    created_at : datetime
    owner_id : int
    owner : userResponse
    #while creating a post we use sqlalchemy model the pydantic model only works with dictionary to use a response of pydantic 
    #we need to create this extra class config with ORM true 
    class Config:
        orm_mode = True

class User(BaseModel):
    email: EmailStr
    password: str

class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    post_id:int
    #conint is constrained int where we can specify the less than eq and greater than equal
    dir: conint(le=1,ge=0)