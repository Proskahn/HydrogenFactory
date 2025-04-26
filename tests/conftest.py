import pytest
import json
import os

@pytest.fixture(autouse=True, scope="function")
def reset_config_json():
    """Reset config.json before each test to ensure a clean state."""
    config_file = "config.json"
    try:
        # Ensure the file is writable
        if os.path.exists(config_file):
            os.chmod(config_file, 0o666)
        with open(config_file, "w") as f:
            json.dump({"electrolyzers": {}, "storages": {}}, f)
    except Exception as e:
        pytest.fail(f"Failed to reset config.json: {str(e)}")
    yield