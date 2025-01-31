from fastapi.testclient import TestClient
from main import app, db
from app.api.v1.endpoints.auth import routes
from app.api.v1.endpoints.auth.hashing import hash_password, verify_password
from app.api.v1.endpoints.auth.jwt_handler import create_access_token
from database import get_db
from app.models import Person
import pytest
client = TestClient(app)


@pytest.fixture
def test_db():
    """Fixture to create and rollback a test database session"""
    db = next(get_db())  # Get a database session
    yield db
    db.rollback()  # Rollback changes after test to maintain clean state

# Test User Registration
def test_get_by_userid(test_db):
    """Test getting a user by userid """
    response = client.get("/api/v1/user/13")
    
    print("------------------------>>>",response.json())  

    assert response.status_code == 200

def test_put_user(test_db):
    """Test updating a user by user ID"""

    existing_user = test_db.query(Person).filter(Person.id == 13).first()
    if not existing_user:
        # Insert a test user if they don't exist
        existing_user = Person(
            id=13,
            firstname="ankitha",
            lastname="reddy",
            is_male=True,
            password_hash="anki123"  #  No need to hash manually
        )
        test_db.add(existing_user)
        test_db.commit()  
    updated_data = {
        "id": 13,
        "firstname": "AnkithaUpdated",
        "lastname": "ReddyUpdated",
        "is_male": True,
        "password_hash": "newpassword123"  
    }
    response = client.put("/api/v1/user/13", json=updated_data)

    print("--------------------------------->", response.json())  # Debugging   
    assert response.status_code == 202
    response_data = response.json()
    assert response_data["id"] == 13
    assert response_data["firstname"] == "AnkithaUpdated"
    assert response_data["lastname"] == "ReddyUpdated"
    assert response_data["is_male"] is True

    

