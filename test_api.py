from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_requires_api_key():
    response = client.post(
        "/analyze-email",
        json={"subject": "Hello", "body": "Normal project update"},
    )
    assert response.status_code == 401


def test_valid_email(api_key):
    response = client.post(
        "/analyze-email",
        headers={"X-API-Key": api_key},
        json={
            "subject": "Meeting tomorrow",
            "body": "Please join the engineering meeting at 10 AM.",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["prediction"] in {"SAFE", "SPAM", "PHISHING"}
    assert 0 <= body["probability"] <= 1
    assert body["action"] in {"ALLOW", "QUARANTINE", "BLOCK"}


def test_empty_body_rejected(api_key):
    response = client.post(
        "/analyze-email",
        headers={"X-API-Key": api_key},
        json={"subject": "Test", "body": ""},
    )
    assert response.status_code == 422


def test_oversized_body_rejected(api_key):
    response = client.post(
        "/analyze-email",
        headers={"X-API-Key": api_key},
        json={"subject": "Test", "body": "A" * 10001},
    )
    assert response.status_code == 422


def test_phishing_gets_high_risk_action(api_key):
    response = client.post(
        "/analyze-email",
        headers={"X-API-Key": api_key},
        json={
            "subject": "Urgent account verification",
            "body": "Your account is suspended. Verify your password immediately.",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["prediction"] == "PHISHING"
    assert body["action"] == "BLOCK"


def test_admin_stats_protected(api_key):
    response = client.get("/admin/stats", headers={"X-API-Key": api_key})
    assert response.status_code == 200
    assert "total_events" in response.json()
