from fastapi.testclient import TestClient

def test_health_endpoint(client: TestClient):
    """
    Test the health check endpoint.
    """
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "is running" in data["message"] 