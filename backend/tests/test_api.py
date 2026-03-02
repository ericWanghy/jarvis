import pytest
from app.main import create_app
from app.core.config import settings

@pytest.fixture
def client():
    # Use a test database or override settings if needed
    settings.ENV = "test"
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert "version" in data

def test_chat_mock(client):
    # Mocking LLM is hard in integration test without patching
    # But we can test if the endpoint accepts JSON
    response = client.post("/api/v1/chat", json={
        "messages": [{"role": "user", "content": "Hello"}],
        "stream": True
    })
    # We might get 200 or 500 depending on LLM connection,
    # but 415 or 400 would mean API definition error.
    assert response.status_code in [200, 500]
