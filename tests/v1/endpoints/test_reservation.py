from fastapi.testclient import TestClient
from main import app, db
from app.api.v1.endpoints.auth import routes
from app.api.v1.endpoints.auth.hashing import hash_password, verify_password
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

def test_get_by_slotid(test_db):
    """Test getting a slot by slotid """
    response = client.get("/api/v1/reservation/?get_all=true")
    
    print("------------------------>>>",response.json())  

    assert response.status_code == 200
