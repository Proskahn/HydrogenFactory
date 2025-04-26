import pytest
import json
from unittest.mock import mock_open, patch
from hydrogen_factory.services.electrolyzer_service import ElectrolyzerService
from hydrogen_factory.models.electrolyzer import ElectrolyzerConfig, ElectrolyzerType

@pytest.fixture
def electrolyzer_service():
    return ElectrolyzerService()

def test_configure_electrolyzer_success(electrolyzer_service):
    config = ElectrolyzerConfig(
        electrolyzer_id="E1",
        type=ElectrolyzerType.PEM,
        capacity=1000.0,
        efficiency_params={"a": -0.1, "b": 0.25, "c": 0.6}
    )
    with patch("builtins.open", mock_open()) as mocked_file:
        electrolyzer_service.configure(config)
        assert electrolyzer_service.electrolyzers["E1"] == config.dict()
        mocked_file().write.assert_called()

def test_configure_electrolyzer_duplicate_id(electrolyzer_service):
    config = ElectrolyzerConfig(
        electrolyzer_id="E1",
        type=ElectrolyzerType.PEM,
        capacity=1000.0,
        efficiency_params={"a": -0.1, "b": 0.25, "c": 0.6}
    )
    electrolyzer_service.configure(config)
    with pytest.raises(ValueError, match="Electrolyzer ID already exists"):
        electrolyzer_service.configure(config)

def test_get_electrolyzer_config_success(electrolyzer_service):
    config = ElectrolyzerConfig(
        electrolyzer_id="E1",
        type=ElectrolyzerType.PEM,
        capacity=1000.0,
        efficiency_params={"a": -0.1, "b": 0.25, "c": 0.6}
    )
    electrolyzer_service.electrolyzers["E1"] = config.dict()
    retrieved = electrolyzer_service.get_config("E1")
    assert retrieved == config

def test_get_electrolyzer_config_not_found(electrolyzer_service):
    with pytest.raises(ValueError, match="Electrolyzer ID not found"):
        electrolyzer_service.get_config("E999")