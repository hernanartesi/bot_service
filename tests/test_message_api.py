import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

def test_message_endpoint_empty_message(client: TestClient):
    """
    Test the message analysis endpoint with an empty message.
    """
    response = client.post(
        "/api/v1/messages/analyze",
        json={"message": ""}
    )
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()

@pytest.mark.asyncio
@patch("app.services.ai_service.AIService.analyze_message")
async def test_message_endpoint_valid_message(mock_analyze, client: TestClient):
    """
    Test the message analysis endpoint with a valid message.
    """
    # Set up the mock
    mock_analyze.return_value = "This is a test response"
    
    # Make the request
    response = client.post(
        "/api/v1/messages/analyze",
        json={"message": "Hello, AI!"}
    )
    
    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "This is a test response"
    
    # Verify the mock was called with the correct argument
    mock_analyze.assert_called_once_with("Hello, AI!") 