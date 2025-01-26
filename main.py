from fastapi import FastAPI
from database import SessionLocal
from app.api.v1.endpoints import user
from app.api.v1.endpoints import reservation
from app.api.v1.endpoints.auth import routes

app = FastAPI()

# Database session
db = SessionLocal()

# Include versioned persons API
app.include_router(user.app, prefix="/api/v1/user", tags=["User"])
app.include_router(reservation.app, prefix="/api/v1/reservation", tags=["Reservation"])
app.include_router(routes.router, prefix="/api/v1/auth", tags=["Auth"])
