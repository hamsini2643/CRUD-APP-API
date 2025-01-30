from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from database import get_db
import app.models as models
from sqlalchemy.orm import Session
from app.api.v1.endpoints.auth.jwt_handler import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime
from fastapi import APIRouter

app = APIRouter()

# OAuth2 scheme to extract the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True  # Enables conversion of ORM models to Pydantic models
        strip_whitespace = True

class SlotCreate(BaseModel):
    start_time: str  # Expecting a string
    end_time: str    # Expecting a string
    person_id: int

class Slot(OurBaseModel):
    id: int
    start_time: str
    end_time: str
    person_id: int

# Dependency to get the current logged-in user
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")

@app.get("/", response_model=list[Slot], status_code=status.HTTP_200_OK)
async def get_slots(
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    person_id: Optional[int] = None,
    sort: Optional[str] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Authentication required
):
    try:
        query = db.query(models.Slots)
        if start_time:
            query = query.filter(models.Slots.start_time == start_time)
        if end_time:
            query = query.filter(models.Slots.end_time == end_time)
        if person_id:
            query = query.filter(models.Slots.person_id == person_id)

        if sort and sort_by:
            sort_column = getattr(models.Slots, sort_by, None)
            if not sort_column:
                raise HTTPException(status_code=400, detail="Invalid sort_by field")

            if sort == "asc":
                query = query.order_by(sort_column.asc())
            elif sort == "desc":
                query = query.order_by(sort_column.desc())

        result = query.all()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''@app.post("/", response_model=Slot, status_code=status.HTTP_201_CREATED)
def add_slot(
    slot: SlotCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Authentication required
    
):
    try:
        user=db.query(models.Person).filter(models.Person.firstname==current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if slot.person_id!=user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to add this slot")
        new_slot = models.Slots(
            start_time=slot.start_time,
            end_time=slot.end_time,
        )
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
        return Slot(
            id=new_slot.id,
            start_time=new_slot.start_time,
            end_time=new_slot.end_time,
            person_id=user.id,
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))'''
@app.post("/", response_model=Slot, status_code=status.HTTP_201_CREATED)
def add_slot(
    slot: SlotCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Authentication required
    
):
    try:
        user=db.query(models.Person).filter(models.Person.firstname==current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if slot.person_id!=user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to add this slot")
        new_slot = models.Slots(
            start_time=slot.start_time,
            end_time=slot.end_time,
            person_id=user.id
        )
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
        return Slot(
            id=new_slot.id,
            start_time=new_slot.start_time,
            end_time=new_slot.end_time,
            person_id=new_slot.person_id,
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/{slot_id}", response_model=Slot, status_code=status.HTTP_202_ACCEPTED)
def update_slot(
    slot_id: int, 
    slot: SlotCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Authentication required
):
    existing_slot = db.query(models.Slots).filter(models.Slots.id == slot_id).first()
    if existing_slot:
        existing_slot.start_time = slot.start_time
        existing_slot.end_time = slot.end_time
        existing_slot.person_id = slot.person_id
        db.commit()
        return existing_slot
    raise HTTPException(status_code=404, detail="Slot not found")

@app.delete("/{slot_id}", status_code=status.HTTP_200_OK)
def delete_slot(
    slot_id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Authentication required
):
    slot = db.query(models.Slots).filter(models.Slots.id == slot_id).first()
    if slot:
        db.delete(slot)
        db.commit()
        return {"message": "Slot deleted successfully"}
    raise HTTPException(status_code=404, detail="Slot not found")

