from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models import Person
from database import get_db
from app.api.v1.endpoints.auth.hashing import hash_password, verify_password
from app.api.v1.endpoints.auth.jwt_handler import create_access_token

router = APIRouter()

class RegisterRequest(BaseModel):
    firstname: str
    lastname: str
    is_male: bool
    password: str

class LoginRequest(BaseModel):
    firstname: str
    password: str
@router.get("/login", response_model=dict)
def login_info():
    # You could return some basic information here, like instructions for logging in
    return {"message": "Use the POST method to login by sending 'firstname' and 'password'."}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    user = db.query(Person).filter(Person.firstname == request.firstname).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(request.password)
    new_user = Person(
        firstname=request.firstname,
        lastname=request.lastname,
        is_male=request.is_male,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.get("/register", response_model=dict)
def register_info():
    # You could return some basic information here, like instructions for registering
    return {"message": "Use the POST method to register by sending 'firstname', 'lastname', 'is_male', and 'password'."}

@router.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Person).filter(Person.firstname == request.firstname).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.firstname})
    return {"access_token": access_token, "token_type": "bearer"}
