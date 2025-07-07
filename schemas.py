from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    gender: str
    password_hash: str


class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True  # Enables conversion of ORM models to Pydantic models


class User(OurBaseModel):
    id: int
    firstname: str
    lastname: str
    gender: str
    #password_hash: str
class User_put(OurBaseModel):
    id: int
    firstname: str
    lastname: str
    gender: str
    password_hash: str

class SlotCreate(BaseModel):
    start_time: str  # Expecting a string
    end_time: str    # Expecting a string
    user_id: int

class Slot(OurBaseModel):
    id: int
    start_time: str
    end_time: str
    user_id: int

