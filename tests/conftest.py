import pytest
from fastapi.testclient import TestClient
from main import app  # Ensure this is the correct import for your FastAPI instance

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
