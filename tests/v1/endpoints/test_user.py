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
    '''assert response.json() == {
    "id": 13,
    "firstname": "ankitha",
    "lastname": "k",
    "is_male": True
}'''

'''def test_put(test_db):

    """Test updating a user by user ID"""

    # ✅ Ensure user exists before updating
    existing_user = test_db.query(Person).filter(Person.id == 13).first()
    assert existing_user is not None  # User should exist before updating

    # ✅ Send `PUT` request with update data
    update_data = {
        "firstname": "ankitha",
        "lastname": "reddy",
        "is_male": True,  # Changed gender field for testing
        "password_hash": "anki123"  # Updated password hash
    }

    response = client.put("/api/v1/user/13", json=update_data)
    
    print("---------------------------->", response.json())  # Debugging

    assert response.status_code == 200  # Expect success

    # ✅ Verify the updated response
    updated_user = response.json()
    assert updated_user["id"] == 13
    assert updated_user["firstname"] == "ankitha"
    assert updated_user["lastname"] == "reddy"
    assert updated_user["is_male"] is False  # Updated value
'''

def test_put_user(test_db):
    """Test updating a user by user ID"""

    # ✅ Ensure user exists before update
    existing_user = test_db.query(Person).filter(Person.id == 13).first()
    if not existing_user:
        # Insert a test user if they don't exist
        existing_user = Person(
            id=13,
            firstname="ankitha",
            lastname="reddy",
            is_male=True,
            password_hash="anki123"  # ✅ No need to hash manually
        )
        test_db.add(existing_user)
        test_db.commit()

    # ✅ Define updated data
    updated_data = {
        "id": 13,
        "firstname": "AnkithaUpdated",
        "lastname": "ReddyUpdated",
        "is_male": True,
        "password_hash": "newpassword123"  # ✅ API will hash this
    }

    # ✅ Make PUT request with body
    response = client.put("/api/v1/user/13", json=updated_data)

    print("--------------------------------->", response.json())  # Debugging

    # ✅ Assert correct response
    assert response.status_code == 202
    response_data = response.json()

    assert response_data["id"] == 13
    assert response_data["firstname"] == "AnkithaUpdated"
    assert response_data["lastname"] == "ReddyUpdated"
    assert response_data["is_male"] is True

    # ✅ Fetch user from DB again to verify update
    #updated_user = test_db.query(Person).filter(Person.id == 13).first()
    #assert updated_user is not None
    #assert updated_user.firstname == "AnkithaUpdated"
    #assert updated_user.lastname == "ReddyUpdated"

    # ✅ Ensure password was updated
    #assert updated_user.password_hash != "newpassword123"  # ❌ Raw password should NOT be stored


