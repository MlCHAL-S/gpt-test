import pytest
import json
from web.api import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data  # Check if HTML content is returned


def test_chat_success(client, requests_mock):
    """Test the /chat endpoint with a successful response."""
    mock_response = {
        "message": {"content": "Hello, how can I help you?"}
    }
    requests_mock.post(
        'http://ollama:11434/api/chat',
        text=json.dumps(mock_response),  # Return the JSON object as a string
        headers={"Content-Type": "application/json"},
    )

    response = client.post("/chat", json={"message": "Hello"})
    assert response.status_code == 200
    assert response.json == {"response": "Hello, how can I help you?"}


def test_chat_missing_message(client):
    """Test the /chat endpoint with a missing message."""
    response = client.post("/chat", json={})
    assert response.status_code == 400
    assert response.json == {"error": "Message is required"}


def test_chat_api_error(client, requests_mock):
    """Test the /chat endpoint when the external API returns an error."""
    requests_mock.post(
        'http://ollama:11434/api/chat',
        status_code=500,
        text="Internal Server Error"
    )

    response = client.post("/chat", json={"message": "Hello"})
    assert response.status_code == 500
    assert "error" in response.json


def test_chat_invalid_json(client):
    """Test the /chat endpoint with invalid JSON."""
    response = client.post(
        "/chat",
        data="invalid",
        content_type="application/json"
    )
    assert response.status_code == 400
