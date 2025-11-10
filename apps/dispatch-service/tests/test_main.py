"""Tests for Dispatch Service."""
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Dispatch Service"
    assert data["status"] == "running"
    assert data["domain"] == "incident-management"


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "dispatch-service"


def test_list_incidents():
    """Test listing incidents (placeholder)."""
    response = client.get("/incidents")
    assert response.status_code == 200
    data = response.json()
    assert "incidents" in data
    assert data["total"] == 0


def test_create_incident():
    """Test creating an incident (placeholder)."""
    incident_data = {
        "title": "Test Incident",
        "description": "Test incident description"
    }
    response = client.post("/incidents", json=incident_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["status"] == "created"


def test_get_incident():
    """Test getting an incident by ID (placeholder)."""
    incident_id = "test-incident-123"
    response = client.get(f"/incidents/{incident_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == incident_id
