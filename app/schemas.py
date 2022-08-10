from datetime import date
from typing import List, Union

from pydantic import BaseModel


class DogBase(BaseModel):
    name: str
    is_adopted: bool

class DogCreate(DogBase):
    picture: str


class Dog(DogBase):
    id: int
    name: str
    picture: str
    is_adopted: bool
    create_date: date
    id_user: int
    
    class Config:
        orm_mode = True 


class UserBase(BaseModel):
    id: int
    name: str
    last_name: Union[str, None] = None
    email: Union[str, None] = None
    dogs: List[Dog]

    class Config:
       orm_mode = True

class User(UserBase):
    id: int
    name: str
    last_name: str
    email: str    
    hashed_password: str
    dogs: List[Dog]=[]

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None           