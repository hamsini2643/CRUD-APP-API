from fastapi import FastAPI, status, HTTPException, Depends

from database import get_db
import app.models as models
import schemas
from typing import Optional
from sqlalchemy.orm import Session
from app.api.v1.endpoints.auth.hashing import hash_password, verify_password
from fastapi import APIRouter

app = APIRouter()
@app.get("/", response_model=list[schemas.User], status_code=status.HTTP_200_OK)
async def get_users(
    firstname: Optional[str] = None,
    lastname: Optional[str] = None,
    gender: Optional[str] = None,
    sort: Optional[str] = None,
    sort_by: Optional[str] = None,
    min_id: Optional[int] = None,
    max_id: Optional[int] = None,
    get_all: Optional[bool] = False,
    db: Session = Depends(get_db),  # Use dependency injection for the session
):
    try:
        # Start with a base query
        query = db.query(models.User)
        if get_all:
            result = query.all()
            return result

        # Apply filters based on optional parameters
        if firstname:
            query = query.filter(models.User.firstname.ilike(f"%{firstname}%"))
        if lastname:
            query = query.filter(models.User.lastname.ilike(f"%{lastname}%"))
        if gender is not None:
            query = query.filter(models.User.gender == gender)

        if sort and sort_by:
            sort_column = getattr(models.User, sort_by, None)
            if not sort_column:
                raise HTTPException(status_code=400, detail="Invalid sort_by field")

            if sort == "asc":
                query = query.order_by(sort_column.asc())
            elif sort == "desc":
                query = query.order_by(sort_column.desc())

        if min_id is not None:
            query = query.filter(models.User.id >= min_id)
        if max_id is not None:
            query = query.filter(models.User.id <= max_id)

        # Execute the query
        result = query.all()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/{id}", response_model=schemas.User, status_code=status.HTTP_200_OK)    
#print("this is id")
def get_single_user(id: int, db: Session = Depends(get_db)):  # Use dependency injection
    try:
        
        get_single_user = db.query(models.User).filter(models.User.id == id).first()
        if not get_single_user:
            raise HTTPException(status_code=404, detail="User not found")
        return get_single_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


'''@app.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def add_user(user: UserCreate, db: Session = Depends(get_db)):  # Use dependency injection
    try:
        new_user = models.User(
            firstname=user.firstname,
            lastname=user.lastname,
            is_male=user.is_male,
            
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Retrieve the auto-generated ID
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))'''


@app.put("/{id}", response_model=schemas.User, status_code=status.HTTP_202_ACCEPTED)
def updateUser(id: int, user: schemas.User_put, db: Session = Depends(get_db)):  # Use dependency injection
    find_user = db.query(models.User).filter(models.User.id == id).first()
    if find_user is not None:
        find_user.firstname = user.firstname
        find_user.lastname = user.lastname
        find_user.gender = user.gender
        #find_user.password_hash = user.password_hash
        if user.password_hash:
            hashed_password = hash_password(user.password_hash)  # Hash the new password
            find_user.password_hash = hashed_password
        db.commit()
        return find_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User with this id not found"
    )


@app.delete("/{id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
def deleteUser(id: int, db: Session = Depends(get_db)):  # Use dependency injection
    find_user = db.query(models.User).filter(models.User.id == id).first()
    if find_user is not None:
        db.delete(find_user)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail="User deleted successfully"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User with this id is either already deleted or not found",
    )


class UpdateUserRequest(schemas.BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    gender: Optional[str] = None


@app.patch("/{id}")
async def update_user(
    id: int,
    user_data: UpdateUserRequest,
    db: Session = Depends(get_db),  # Use dependency injection
):
    # Fetch the user by ID
    user = db.query(models.User).filter(models.User.id == id).first()

    # Check if the user exists
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields if provided in the request
    if user_data.firstname is not None:
        user.firstname = user_data.firstname
    if user_data.lastname is not None:
        user.lastname = user_data.lastname
    if user_data.gender is not None:
        user.gender = user_data.gender

    # Commit the changes to the database
    db.commit()
    db.refresh(user)  # Refresh the instance to reflect the changes

    return user


@app.get("/{user_id}/reservations", response_model=list[schemas.Slot], status_code=status.HTTP_200_OK)
async def get_reservations_by_user_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Fetch all reservations for a specific user by their user_id.
    """
    try:
        reservations = db.query(models.Slots).filter(models.Slots.user_id == user_id).all()

        if not reservations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No reservations found for user with ID {user_id}"
            )

        return reservations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{user_id}/reservations/{slot_id}", response_model=schemas.Slot, status_code=status.HTTP_200_OK)
async def get_single_reservation_for_user(
    user_id: int,
    slot_id: int,
    db: Session = Depends(get_db)
):
    """
    Fetch a single reservation for a specific user by user_id and slot_id.
    """
    try:
        reservation = (
            db.query(models.Slots)
            .filter(models.Slots.user_id == user_id, models.Slots.id == slot_id)
            .first()
        )

        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reservation with ID {slot_id} not found for user with ID {user_id}"
            )

        return reservation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


