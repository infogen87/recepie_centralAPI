from pydantic import BaseModel, EmailStr
import datetime
from typing import Optional



class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    image_url: str
    description: str
    # created_at


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str



class User(UserBase):
    id: int


class UpdateUser(BaseModel):
    username: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None

    
      

