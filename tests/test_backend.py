import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_dashboard_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Intelligent Dead Reckoning" in response.text

def test_api_status(client):
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert "system" in data
    assert "calibration_profile" in data
    assert "current_ekf_state" in data

def test_toggle_outage(client):
    response = client.post("/api/simulation/toggle_outage", json={"outage_active": True})
    assert response.status_code == 200
    data = response.json()
    assert data["force_outage"] is True

    # Toggle back
    response = client.post("/api/simulation/toggle_outage", json={"outage_active": False})
    assert response.status_code == 200
    assert response.json()["force_outage"] is False

def test_telemetry_feed(client):
    payload = {
        "imu": {
            "timestamp": 1.0,
            "accel_x": 0.5,
            "accel_y": 0.0,
            "accel_z": 9.81,
            "gyro_x": 0.0,
            "gyro_y": 0.0,
            "gyro_z": 0.01
        },
        "gnss": {
            "timestamp": 1.0,
            "latitude": 12.9716,
            "longitude": 77.5946,
            "speed_ms": 5.0,
            "bearing_deg": 45.0,
            "accuracy_m": 2.0
        },
        "simulate_outage": False
    }
    response = client.post("/api/telemetry/feed", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "estimated_lat" in data
    assert "estimated_lon" in data
    assert "velocity_kmh" in data
    assert "calibration_profile" in data
    assert data["outage_active"] is False

def test_reset_simulation(client):
    response = client.post("/api/simulation/reset")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
