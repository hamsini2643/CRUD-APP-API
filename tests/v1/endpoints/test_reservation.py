from fastapi.testclient import TestClient
from main import app, db
from app.api.v1.endpoints.auth import routes
from app.api.v1.endpoints.auth.hashing import hash_password, verify_password
from app.api.v1.endpoints.auth.jwt_handler import create_access_token
from database import get_db
from app.models import Person
import pytest
client = TestClient(app)