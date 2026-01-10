import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_concurrent_requests():
    """
    Test sending multiple requests concurrently to simulate load.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        tasks = []
        for i in range(50):
            tasks.append(
                ac.post(
                    "/api/send-email",
                    json={
                        "recipient": f"test{i}@example.com",
                        "subject": f"Subject {i}",
                        "message": f"Message {i}",
                    },
                )
            )
        
        responses = await asyncio.gather(*tasks)
        
        for response in responses:
            assert response.status_code == 200
            assert response.json() == {"status": "success", "message": "Email sent successfully"}

@pytest.mark.asyncio
async def test_rapid_fire_requests():
    """
    Test sending requests in rapid succession.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for i in range(20):
            response = await ac.post(
                "/api/send-email",
                json={
                    "recipient": "test@example.com",
                    "subject": "Rapid Fire",
                    "message": f"Message {i}",
                },
            )
            assert response.status_code == 200

@pytest.mark.asyncio
async def test_malformed_json():
    """
    Test sending malformed JSON data.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/send-email",
            content="not json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_large_payload():
    """
    Test sending a very large payload.
    """
    large_message = "x" * 1024 * 1024  # 1MB message
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/send-email",
            json={
                "recipient": "test@example.com",
                "subject": "Large Payload",
                "message": large_message,
            },
        )
        # Depending on server config, this might pass or fail (413).
        # Assuming default FastAPI/Starlette config handles it or passes it through.
        # We expect 200 if no limit is explicitly set, or 422/413 if there is.
        # For this test, we just ensure it doesn't crash the server (500).
        assert response.status_code != 500