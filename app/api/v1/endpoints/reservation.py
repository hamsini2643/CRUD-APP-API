from fastapi import FastAPI, status, HTTPException, Depends 
from pydantic import BaseModel
from database import get_db
import app.models as models
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter
from datetime import datetime

app = APIRouter()

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

@app.get("/", response_model=list[Slot], status_code=status.HTTP_200_OK)
async def get_slots(
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    person_id: Optional[int] = None,
    sort: Optional[str] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db),
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

@app.get("/{slot_id}", response_model=Slot, status_code=status.HTTP_200_OK)
def get_single_slot(slot_id: int, db: Session = Depends(get_db)):
    try:
        slot = db.query(models.Slots).filter(models.Slots.id == slot_id).first()
        if not slot:
            raise HTTPException(status_code=404, detail="Slot not found")
        return slot
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/", response_model=Slot)
def add_slot(slot: SlotCreate, db: Session = Depends(get_db)):
    try:
        new_slot = models.Slots(
            start_time=slot.start_time,
            end_time=slot.end_time,
            person_id=slot.person_id,
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
    
@app.put("/{slot_id}", response_model=Slot)
def update_slot(slot_id: int, slot: SlotCreate, db: Session = Depends(get_db)):
    existing_slot = db.query(models.Slots).filter(models.Slots.id == slot_id).first()
    if existing_slot:
        existing_slot.start_time = slot.start_time
        existing_slot.end_time = slot.end_time
        existing_slot.person_id = slot.person_id
        db.commit()
        return existing_slot
    raise HTTPException(status_code=404, detail="Slot not found")

@app.delete("/{slot_id}", response_model=Slot)
def delete_slot(slot_id: int, db: Session = Depends(get_db)):
    slot = db.query(models.Slots).filter(models.Slots.id == slot_id).first()
    if slot:
        db.delete(slot)
        db.commit()
        raise HTTPException(status_code=200, detail="Slot deleted successfully")
    raise HTTPException(status_code=404, detail="Slot not found")

@app.get("/user/{person_id}/reservations", response_model=list[Slot], status_code=status.HTTP_200_OK)
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

@app.get("/user/{person_id}/reservations/{slot_id}", response_model=Slot, status_code=status.HTTP_200_OK)
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