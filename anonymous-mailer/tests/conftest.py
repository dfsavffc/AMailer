import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from main import app, limiter
from app.core.config import settings

@pytest.fixture(scope="module")
def client():
    # Force mock email for tests
    settings.MOCK_EMAIL = True
    # Disable rate limiter for tests
    limiter.enabled = False
    with TestClient(app) as c:
        yield c
    limiter.enabled = True

import random

@pytest_asyncio.fixture(scope="function")
async def async_client():
    # Force mock email for tests
    settings.MOCK_EMAIL = True
    # Disable rate limiter for tests
    limiter.enabled = False
    random_ip = f"127.0.0.{random.randint(1, 255)}"
    transport = ASGITransport(app=app, client=(random_ip, 12345))
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    limiter.enabled = True