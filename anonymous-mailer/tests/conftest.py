import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.config import settings

@pytest.fixture(scope="module")
def client():
    # Force mock email for tests
    settings.MOCK_EMAIL = True
    with TestClient(app) as c:
        yield c