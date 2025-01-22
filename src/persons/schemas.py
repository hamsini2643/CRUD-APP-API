from pydantic import BaseModel

class PersonCreate(BaseModel):
    firstname: str
    lastname: str
    is_male: bool
class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True  # Enables conversion of ORM models to Pydantic models

class Person(OurBaseModel):
    id: int
    firstname: str
    lastname: str
    is_male: bool