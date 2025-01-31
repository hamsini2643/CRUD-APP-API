from fastapi import FastAPI, status, HTTPException, Depends

from database import get_db
import app.models as models
import schemas
from typing import Optional
from sqlalchemy.orm import Session
from app.api.v1.endpoints.auth.hashing import hash_password, verify_password
from fastapi import APIRouter

app = APIRouter()
@app.get("/", response_model=list[schemas.Person], status_code=status.HTTP_200_OK)
async def get_persons(
    firstname: Optional[str] = None,
    lastname: Optional[str] = None,
    is_male: Optional[bool] = None,
    sort: Optional[str] = None,
    sort_by: Optional[str] = None,
    min_id: Optional[int] = None,
    max_id: Optional[int] = None,
    get_all: Optional[bool] = False,
    db: Session = Depends(get_db),  # Use dependency injection for the session
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


@app.get("/{id}", response_model=schemas.Person, status_code=status.HTTP_200_OK)    
#print("this is id")
def get_single_person(id: int, db: Session = Depends(get_db)):  # Use dependency injection
    try:
        
        get_single_person = db.query(models.Person).filter(models.Person.id == id).first()
        if not get_single_person:
            raise HTTPException(status_code=404, detail="Person not found")
        return get_single_person
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


'''@app.post("/", response_model=Person, status_code=status.HTTP_201_CREATED)
def add_person(person: PersonCreate, db: Session = Depends(get_db)):  # Use dependency injection
    try:
        new_person = models.Person(
            firstname=person.firstname,
            lastname=person.lastname,
            is_male=person.is_male,
            
        )
        db.add(new_person)
        db.commit()
        db.refresh(new_person)  # Retrieve the auto-generated ID
        return new_person
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))'''


@app.put("/{id}", response_model=schemas.Person, status_code=status.HTTP_202_ACCEPTED)
def updatePerson(id: int, person: schemas.Person_put, db: Session = Depends(get_db)):  # Use dependency injection
    find_person = db.query(models.Person).filter(models.Person.id == id).first()
    if find_person is not None:
        find_person.firstname = person.firstname
        find_person.lastname = person.lastname
        find_person.is_male = person.is_male
        #find_person.password_hash = person.password_hash
        if person.password_hash:
            hashed_password = hash_password(person.password_hash)  # Hash the new password
            find_person.password_hash = hashed_password
        db.commit()
        return find_person
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Person with this id not found"
    )


@app.delete("/{id}", response_model=schemas.Person, status_code=status.HTTP_200_OK)
def deletePerson(id: int, db: Session = Depends(get_db)):  # Use dependency injection
    find_person = db.query(models.Person).filter(models.Person.id == id).first()
    if find_person is not None:
        db.delete(find_person)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail="Person deleted successfully"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Person with this id is either already deleted or not found",
    )


class UpdatePersonRequest(schemas.BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    is_male: Optional[bool] = None


@app.patch("/{id}")
async def update_person(
    id: int,
    person_data: UpdatePersonRequest,
    db: Session = Depends(get_db),  # Use dependency injection
):
    # Fetch the person by ID
    person = db.query(models.Person).filter(models.Person.id == id).first()

    # Check if the person exists
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    # Update fields if provided in the request
    if person_data.firstname is not None:
        person.firstname = person_data.firstname
    if person_data.lastname is not None:
        person.lastname = person_data.lastname
    if person_data.is_male is not None:
        person.is_male = person_data.is_male

    # Commit the changes to the database
    db.commit()
    db.refresh(person)  # Refresh the instance to reflect the changes

    return person


@app.get("/{person_id}/reservations", response_model=list[schemas.Slot], status_code=status.HTTP_200_OK)
async def get_reservations_by_user_id(
    person_id: int,
    db: Session = Depends(get_db)
):
    """
    Fetch all reservations for a specific user by their person_id.
    """
    try:
        reservations = db.query(models.Slots).filter(models.Slots.person_id == person_id).all()

        if not reservations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No reservations found for user with ID {person_id}"
            )

        return reservations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{person_id}/reservations/{slot_id}", response_model=schemas.Slot, status_code=status.HTTP_200_OK)
async def get_single_reservation_for_user(
    person_id: int,
    slot_id: int,
    db: Session = Depends(get_db)
):
    """
    Fetch a single reservation for a specific user by person_id and slot_id.
    """
    try:
        reservation = (
            db.query(models.Slots)
            .filter(models.Slots.person_id == person_id, models.Slots.id == slot_id)
            .first()
        )

        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reservation with ID {slot_id} not found for user with ID {person_id}"
            )

        return reservation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


