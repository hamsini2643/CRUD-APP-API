from pydantic import BaseModel, Field
from typing import Optional

class PersonCreate(BaseModel):
    firstname: str
    lastname: str
    is_male: bool
    password_hash: str


class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True  # Enables conversion of ORM models to Pydantic models


class Person(OurBaseModel):
    id: int
    firstname: str
    lastname: str
    is_male: bool
    #password_hash: str
class Person_put(OurBaseModel):
    id: int
    firstname: str
    lastname: str
    is_male: bool
    password_hash: str

class SlotCreate(BaseModel):
    start_time: str  # Expecting a string
    end_time: str    # Expecting a string
    person_id: int

class Slot(OurBaseModel):
    id: int
    start_time: str
    end_time: str
    person_id: int

