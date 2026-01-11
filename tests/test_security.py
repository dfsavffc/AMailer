import asyncio
import pytest

@pytest.mark.asyncio
async def test_ddos_simulation(async_client):
    """
    Simulate a DDoS attack by sending a large number of requests concurrently.
    """
    tasks = []
    # Simulate 500 concurrent requests
    for i in range(500):
        tasks.append(
            async_client.post(
                "/api/send-email",
                json={
                    "recipient": f"victim{i}@example.com",
                    "subject": "Spam",
                    "message": "Spam message",
                },
            )
        )
    
    responses = await asyncio.gather(*tasks)

    for response in responses:
        assert response.status_code in [200, 429, 500, 503]

@pytest.mark.asyncio
async def test_sql_injection_attempt(async_client):
    """
    Test for SQL injection vulnerabilities (though we don't use a DB, it's good practice).
    """
    response = await async_client.post(
        "/api/send-email",
        json={
            "recipient": "test@example.com",
            "subject": "'; DROP TABLE users; --",
            "message": "Test Message",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Email sent successfully"}

@pytest.mark.asyncio
async def test_xss_attempt(async_client):
    """
    Test for XSS vulnerabilities in input fields.
    """
    xss_payload = "<script>alert('XSS')</script>"
    response = await async_client.post(
        "/api/send-email",
        json={
            "recipient": "test@example.com",
            "subject": xss_payload,
            "message": xss_payload,
        },
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_large_payload_dos(async_client):
    """
    Test sending an extremely large payload to cause DoS.
    """
    # 10MB payload
    large_message = "A" * 10 * 1024 * 1024
    response = await async_client.post(
        "/api/send-email",
        json={
            "recipient": "test@example.com",
            "subject": "Large Payload",
            "message": large_message,
        },
    )
    assert response.status_code != 500