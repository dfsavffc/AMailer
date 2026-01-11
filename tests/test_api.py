def test_send_email_success(client):
    response = client.post(
        "/api/send-email",
        json={
            "recipient": "test@example.com",
            "subject": "Test Subject",
            "message": "Test Message",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Email sent successfully",
    }


def test_send_email_invalid_email(client):
    response = client.post(
        "/api/send-email",
        json={
            "recipient": "invalid-email",
            "subject": "Test Subject",
            "message": "Test Message",
        },
    )
    assert response.status_code == 422


def test_send_email_missing_field(client):
    response = client.post(
        "/api/send-email",
        json={
            "recipient": "test@example.com",
            "message": "Test Message",
        },
    )
    assert response.status_code == 422


def test_send_email_empty_fields(client):
    response = client.post(
        "/api/send-email",
        json={
            "recipient": "test@example.com",
            "subject": "",
            "message": "",
        },
    )
    assert response.status_code in [200, 422]


def test_send_email_long_content(client):
    long_subject = "a" * 200
    long_message = "b" * 5000
    response = client.post(
        "/api/send-email",
        json={
            "recipient": "test@example.com",
            "subject": long_subject,
            "message": long_message,
        },
    )
    assert response.status_code == 200