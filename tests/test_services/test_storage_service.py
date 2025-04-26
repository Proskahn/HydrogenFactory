import pytest
import json
from unittest.mock import mock_open, patch
from hydrogen_factory.services.storage_service import StorageService
from hydrogen_factory.models.storage import StorageConfig

@pytest.fixture
def storage_service():
    return StorageService()

def test_configure_storage_success(storage_service):
    config = StorageConfig(
        storage_id="S1",
        max_capacity=100.0
    )
    with patch("builtins.open", mock_open()) as mocked_file:
        storage_service.configure(config)
        assert storage_service.storages["S1"] == config.dict()
        mocked_file().write.assert_called()

def test_configure_storage_duplicate_id(storage_service):
    config = StorageConfig(
        storage_id="S1",
        max_capacity=100.0
    )
    storage_service.configure(config)
    with pytest.raises(ValueError, match="Storage ID already exists"):
        storage_service.configure(config)

def test_get_storage_config_success(storage_service):
    config = StorageConfig(
        storage_id="S1",
        max_capacity=100.0
    )
    storage_service.storages["S1"] = config.dict()
    retrieved = storage_service.get_config("S1")
    assert retrieved == config

def test_get_storage_config_not_found(storage_service):
    with pytest.raises(ValueError, match="Storage ID not found"):
        storage_service.get_config("S999")