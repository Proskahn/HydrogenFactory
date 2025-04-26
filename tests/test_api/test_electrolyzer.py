import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import pytest
import json
from fastapi.testclient import TestClient
from hydrogen_factory.main import app
from hydrogen_factory.models.electrolyzer import ElectrolyzerConfig, ElectrolyzerType

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_config_json():
    """Reset config.json before each test to ensure a clean state."""
    try:
        with open("config.json", "w") as f:
            json.dump({"electrolyzers": {}, "storages": {}}, f)
    except Exception as e:
        pytest.fail(f"Failed to reset config.json: {str(e)}")
    yield

def test_configure_electrolyzer_success():
    payload = {
        "electrolyzer_id": "E1",
        "type": "PEM",
        "capacity": 1000.0,
        "efficiency": 0.02
    }
    response = client.post("/api/electrolyzer/configure", json=payload)
    if response.status_code != 200:
        print(f"Error response: {response.json()}")
    assert response.status_code == 200
    assert response.json() == payload

def test_configure_electrolyzer_duplicate_id():
    payload = {
        "electrolyzer_id": "E1",
        "type": "ALKALINE",
        "capacity": 500.0,
        "efficiency": 0.02
    }
    response = client.post("/api/electrolyzer/configure", json=payload)
    assert response.status_code == 400
    assert "Electrolyzer ID already exists" in response.json()["detail"]

def test_configure_electrolyzer_invalid_capacity():
    payload = {
        "electrolyzer_id": "E2",
        "type": "PEM",
        "capacity": -100.0,
        "efficiency": 0.02
    }
    response = client.post("/api/electrolyzer/configure", json=payload)
    assert response.status_code == 422
    assert "greater than 0" in response.json()["detail"][0]["msg"]