from fastapi import FastAPI
from src.persons.routes import person_router
version="v1"
app=FastAPI(
    
    title="Person API",
    description="A simple API for managing persons",
    version=version
)
app.include_router(person_router,prefix=f"/api/{version}/persons",tags=['persons'])