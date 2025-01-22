from fastapi import FastAPI
from database import SessionLocal
from app.api.v1.endpoints import user

app = FastAPI()

# Database session
db = SessionLocal()

# Include versioned persons API
app.include_router(user.app, prefix="/api/v1/user", tags=["User"])
