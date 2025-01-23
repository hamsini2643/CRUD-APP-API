

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from database import SessionLocal
import app.models as models
from typing import Optional

from fastapi import APIRouter

app = APIRouter()
class PersonCreate(BaseModel):
    firstname: str
    lastname: str
    is_male: bool
class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True  # Enables conversion of ORM models to Pydantic models

class Person(OurBaseModel):
    id: int
    firstname: str
    lastname: str
    is_male: bool

# Create a database session instance
db = SessionLocal()
@app.get("/", response_model=list[Person], status_code=status.HTTP_200_OK)
async def get_persons(
    firstname: Optional[str] = None,
    lastname: Optional[str] = None,
    is_male: Optional[bool] = None,
    sort: Optional[str] = None,
    sort_by: Optional[str] = None,
    min_id: Optional[int] = None,
    max_id: Optional[int] = None,
    get_all: Optional[bool] = False,
):
    try:
        # Start with a base query
        query = db.query(models.Person)
        if get_all:
            result = query.all()
            return result
        
        # Apply filters based on optional parameters
        if firstname:
            query = query.filter(models.Person.firstname.ilike(f"%{firstname}%"))
        if lastname:
            query = query.filter(models.Person.lastname.ilike(f"%{lastname}%"))
        if is_male is not None:
            query = query.filter(models.Person.is_male == is_male)
        '''if sort == "asc":
            query = query.order_by(models.Person.firstname.asc())
        elif sort == "desc":
            query = query.order_by(models.Person.firstname.desc())'''
        if sort and sort_by:
            sort_column = getattr(models.Person, sort_by, None)
            if not sort_column:
                raise HTTPException(status_code=400, detail="Invalid sort_by field")
            
            if sort == "asc":
                query = query.order_by(sort_column.asc())
            elif sort == "desc":
                query = query.order_by(sort_column.desc())
        if min_id is not None:
            query = query.filter(models.Person.id >= min_id)
        if max_id is not None:
            query = query.filter(models.Person.id <= max_id)
        
        # Execute the query
        result = query.all()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''@app.get('/', response_model=list[Person], status_code=status.HTTP_200_OK)
def get_all_persons():
    try:
        persons = db.query(models.Person).all()
        return persons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))'''
@app.get('/{person_id}', response_model=Person, status_code=status.HTTP_200_OK)
def get_single_person(person_id:int):
    try:
        get_single_person = db.query(models.Person).filter(models.Person.id==person_id).first()
        return get_single_person
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/', response_model=Person, status_code=status.HTTP_201_CREATED)
def add_person(person: PersonCreate):
    try:
        new_person = models.Person(
            firstname=person.firstname,
            lastname=person.lastname,
            is_male=person.is_male
        )
        db.add(new_person)
        db.commit()
        db.refresh(new_person)  # Retrieve the auto-generated ID
        return new_person
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/{person_id}',response_model=Person,status_code=status.HTTP_202_ACCEPTED)
def updatePerson(person_id:int,person:Person):
    find_person=db.query(models.Person).filter(models.Person.id==person_id).first()
    if find_person is not None:
        find_person.id=person.id
        find_person.firstname=person.firstname
        find_person.lastname=person.lastname
        find_person.lastname=person.lastname
        find_person.is_male=person.is_male
        db.commit()
        return find_person
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Person with this id not found")

@app.delete("/{person_id}",response_model=Person,status_code=200)
def deletePerson(person_id:int):
    find_person=db.query(models.Person).filter(models.Person.id==person_id).first()
    if find_person is not None:

        db.delete(find_person)
        db.commit()
        #return find_person
        raise HTTPException(status_code=status.HTTP_200_OK,detail="Person deleted successfully")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Person with this id is either already deleted or not found")
