

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from database import SessionLocal
import models

app = FastAPI()

class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True  # Enables conversion of ORM models to Pydantic models

class Person(OurBaseModel):
    id: int
    firstname: str
    lastname: str
    isMale: bool

# Create a database session instance
db = SessionLocal()

@app.get('/', response_model=list[Person], status_code=status.HTTP_200_OK)
def get_all_persons():
    try:
        persons = db.query(models.Person).all()
        return persons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get('/get_by_id/{person_id}', response_model=Person, status_code=status.HTTP_200_OK)
def get_single_person(person_id:int):
    try:
        get_single_person = db.query(models.Person).filter(models.Person.id==person_id).first()
        return get_single_person
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/addperson', response_model=Person, status_code=status.HTTP_201_CREATED)
def add_person(person: Person):
    try:
        new_person = models.Person(
            id=person.id,
            firstname=person.firstname,
            lastname=person.lastname,
            isMale=person.isMale
        )
        find_person=db.query(models.Person).filter(models.Person.id==person.id).first()
        if find_person is not None:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Person with this id already exists")
        


        db.add(new_person)
        db.commit()
        #db.refresh(new_person)  # Refresh the instance to get updated data (e.g., auto-generated fields)
        return new_person
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
@app.put('/update_person/{person_id}',response_model=Person,status_code=status.HTTP_202_ACCEPTED)
def updatePerson(person_id:int,person:Person):
    find_person=db.query(models.Person).filter(models.Person.id==person_id).first()
    if find_person is not None:
        find_person.id=person.id
        find_person.firstname=person.firstname
        find_person.lastname=person.lastname
        find_person.lastname=person.lastname
        find_person.isMale=person.isMale
        db.commit()
        return find_person
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Person with this id not found")

@app.delete("/delete_person/{person_id}",response_model=Person,status_code=200)
def deletePerson(person_id:int):
    find_person=db.query(models.Person).filter(models.Person.id==person_id).first()
    if find_person is not None:

        db.delete(find_person)
        db.commit()
        #return find_person
        raise HTTPException(status_code=status.HTTP_200_OK,detail="Person deleted successfully")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Person with this id is either already deleted or not found")

