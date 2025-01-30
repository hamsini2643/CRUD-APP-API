from fastapi.testclient import TestClient
from main import app, db
from app.api.v1.endpoints.auth import routes
from app.api.v1.endpoints.auth.hashing import hash_password, verify_password
from app.api.v1.endpoints.auth.jwt_handler import create_access_token
from database import get_db
from app.models import Person
import pytest
client = TestClient(app)


# Create a fixture to provide a test database session
@pytest.fixture
def test_db():
    """Fixture to create and rollback a test database session"""
    db = next(get_db())  # Get a database session
    yield db
    db.rollback()  # Rollback changes after test to maintain clean state

# Test User Registration
def test_register_user(test_db):
    """Test registering a user """
    test_db.query(Person).filter(Person.firstname == "jam").delete()
    test_db.commit()
    password = "jam123"  # Plain password
    response = client.post("/api/v1/auth/register", json={
        "firstname": "jam",
        "lastname": "r",
        "password": password,  # Sent as plain text (API should hash it)
        "is_male": True  # Correct boolean type
    })
    print("------------------------>>>",response.json())  # Debugging: See API error message

    assert response.status_code == 201  # Ensure success
    assert response.json() == {"message": "User registered successfully"}

    # Verify user is saved in DB with hashed password
    user_in_db = test_db.query(Person).filter(Person.firstname == "jam").first()
    assert user_in_db is not None
    assert verify_password(password, user_in_db.password_hash)  # Ensure hash matches


#  Test User Login successfullly 
def test_login_user(test_db):
    """Test login with correct password"""

    password = "jam123"
    hashed_password = hash_password(password)  # Hash password before saving

    # Manually insert a test user in the database
    test_user = test_db.query(Person).filter(Person.firstname == "jam").first()
    assert test_user is not None
    

    # Attempt to login
    response = client.post("/api/v1/auth/login", json={
        "firstname": "jam",
        "password": password  # Sending plain password
    })
    print("------------------------>>>",response.json())  # Debugging: See API error message

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user_id"] == test_user.id

#test login with wrong password
def test_login_user_wrong(test_db):
    """Test login with wrong password"""

    password = "randompassword"
    hashed_password = hash_password(password)  # Hash password before saving

    # Manually insert a test user in the database
    test_user = test_db.query(Person).filter(Person.firstname == "jam").first()
    assert test_user is not None
    

    # Attempt to login
    response = client.post("/api/v1/auth/login", json={
        "firstname": "jam",
        "password": password  # Sending plain password
    })
    print("------------------------>>>",response.json())  # Debugging: See API error message

    assert response.status_code == 401
    data = response.json()
    assert data=={'detail': 'Invalid credentials'}
    #assert data["token_type"] == "bearer"
    #assert data["user_id"] == test_user.id

def test_login_nonexistent_user(client):
    """Test login with a user that does not exist"""

    response = client.post("/api/v1/auth/login", json={
        "firstname": "ghost",
        "password": "randompassword"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
