import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import pytest
import json
from fastapi.testclient import TestClient
from hydrogen_factory.main import app
from hydrogen_factory.models.electrolyzer import ElectrolyzerConfig, ElectrolyzerType
from hydrogen_factory.models.storage import StorageConfig

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

def test_optimize_schedule_success():
    electrolyzer_payload = {
        "electrolyzer_id": "E1",
        "type": "PEM",
        "capacity": 1000.0,
        "efficiency": 0.02
    }
    client.post("/api/electrolyzer/configure", json=electrolyzer_payload)

    storage_payload = {
        "storage_id": "S1",
        "max_capacity": 100.0
    }
    client.post("/api/storage/configure", json=storage_payload)

    optimize_payload = {
        "electrolyzer_id": "E1",
        "storage_id": "S1"
    }
    response = client.post("/api/schedule/optimize", json=optimize_payload)
    assert response.status_code == 200
    result = response.json()
    assert len(result["power_schedule"]) == 24
    assert len(result["hydrogen_produced"]) == 24
    assert len(result["storage_levels"]) == 24
    assert isinstance(result["total_cost"], float)

def test_optimize_schedule_missing_electrolyzer():
    optimize_payload = {
        "electrolyzer_id": "E999",
        "storage_id": "S1"
    }
    response = client.post("/api/schedule/optimize", json=optimize_payload)
    assert response.status_code == 400
    assert "Electrolyzer ID not found" in response.json()["detail"]

def test_optimize_schedule_missing_storage():
    optimize_payload = {
        "electrolyzer_id": "E1",
        "storage_id": "S999"
    }
    response = client.post("/api/schedule/optimize", json=optimize_payload)
    assert response.status_code == 400
    assert "Storage ID not found" in response.json()["detail"]