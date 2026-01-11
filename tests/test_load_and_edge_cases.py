import asyncio
import pytest

@pytest.mark.asyncio
async def test_concurrent_requests(async_client):
    """
    Test sending multiple requests concurrently to simulate load.
    """
    tasks = []
    for i in range(50):
        tasks.append(
            async_client.post(
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
async def test_rapid_fire_requests(async_client):
    """
    Test sending requests in rapid succession.
    """
    for i in range(20):
        response = await async_client.post(
            "/api/send-email",
            json={
                "recipient": "test@example.com",
                "subject": "Rapid Fire",
                "message": f"Message {i}",
            },
        )
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_malformed_json(async_client):
    """
    Test sending malformed JSON data.
    """
    response = await async_client.post(
        "/api/send-email",
        content="not json",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_large_payload(async_client):
    """
    Test sending a very large payload.
    """
    large_message = "x" * 1024 * 1024  # 1MB message
    response = await async_client.post(
        "/api/send-email",
        json={
            "recipient": "test@example.com",
            "subject": "Large Payload",
            "message": large_message,
        },
    )
    assert response.status_code != 500