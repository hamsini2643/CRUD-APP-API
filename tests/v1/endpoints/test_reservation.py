from fastapi.testclient import TestClient
from main import app
from app.api.v1.endpoints.auth.hashing import hash_password
from app.api.v1.endpoints.auth.jwt_handler import create_access_token
from database import get_db
from app.models import User
import pytest

client = TestClient(app)

@pytest.fixture
def test_db():
    """Fixture to create and rollback a test database session"""
    db = next(get_db())  # Get a database session
    yield db
    db.rollback()  # Rollback changes after test to maintain clean state

def get_token(test_db):
    """Test login with correct password"""
    password = "jam123"
    hashed_password = hash_password(password)  # Hash password before saving

    # Manually insert a test user in the database
    test_user = test_db.query(User).filter(User.firstname == "jam").first()
    assert test_user is not None
    response = client.post("/api/v1/auth/login", json={
        "firstname": "jam",
        "password": password  # Sending plain password
    })
    print("------------------------>>>", response.json())  # Debugging: See API error message

    assert response.status_code == 200
    data = response.json()
    print('---------------------------------------------------------------->',data)
    assert "access_token" in data
    #assert data["token_type"] == "bearer"
    #assert data["user_id"] == test_user.id
    return data["access_token"]  # Return token

def get_header(token):
    headers = {"Authorization": f"Bearer {token}"}
    return headers

def test_add_slot(test_db):
    token = get_token(test_db)  # Fetch the token using the test_db fixture
    headers = get_header(token)
    
    # Assuming the route for adding a slot is "/api/v1/slots/"
    slot_data = {"start_time": "10:00", "end_time": "11:00", "user_id": 3}
    response = client.post("/api/v1/reservation/", json=slot_data, headers=headers)
    
    assert response.status_code == 201
    assert response.json()["start_time"] == "10:00"
    assert response.json()["end_time"] == "11:00"
def test_get_slots(test_db):
    token = get_token(test_db)  # Fetch the token using the test_db fixture
    headers = get_header(token)

    # Assuming the route for getting slots is "/api/v1/slots/"
    response = client.get("/api/v1/reservation/", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) > 0



def test_update_slot(test_db):
    token = get_token(test_db)  # Fetch the token using the test_db fixture
    headers = get_header(token)
    # Assuming the route for updating a slot is "/api/v1/slots/{slot_id}"
    slot_id = 2  # Replace with a valid slot ID from your database
    updated_data = {"id":1,"user_id":2,"start_time": "10:00", "end_time": "11:00"}
    response = client.put(f"/api/v1/reservation/{slot_id}", json=updated_data, headers=headers)
    assert response.status_code == 202
    #assert response.json()["start_time"] == "10:00"
    #assert response.json()["end_time"] == "11:00"


def test_delete_slot(test_db):
    token = get_token(test_db)  # Fetch the token using the test_db fixture
    headers = get_header(token)
    # Assuming the route for deleting a slot is "/api/v1/slots/{slot_id}"
    slot_id = 2  # Replace with a valid slot ID from your database
    response = client.delete(f"/api/v1/reservation/{slot_id}", headers=headers)
    assert response.status_code == 200

'''def test_put_user(test_db):
    """Test updating a user by user ID"""

    existing_user = test_db.query(User).filter(User.id == 13).first()
    if not existing_user:
        # Insert a test user if they don't exist
        existing_user = User(
            id=13,
            firstname="ankitha",
            lastname="reddy",
            gender="female",
            password_hash="anki123"  #  No need to hash manually
        )
        test_db.add(existing_user)
        test_db.commit()  
    updated_data = {
        "id": 13,
        "firstname": "AnkithaUpdated",
        "lastname": "ReddyUpdated",
        "gender": "female",
        "password_hash": "newpassword123"  
    }
    response = client.put("/api/v1/user/13", json=updated_data)

    print("--------------------------------->", response.json())  # Debugging   
    assert response.status_code == 202
    response_data = response.json()'''
    


        



