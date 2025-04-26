import pytest
import numpy as np
from unittest.mock import MagicMock
from hydrogen_factory.services.optimization_service import OptimizationService
from hydrogen_factory.models.electrolyzer import ElectrolyzerConfig, ElectrolyzerType
from hydrogen_factory.models.storage import StorageConfig
from hydrogen_factory.models.schedule import OptimizationInput, OptimizationOutput

@pytest.fixture
def optimization_service():
    electrolyzer_service = MagicMock()
    storage_service = MagicMock()
    return OptimizationService(electrolyzer_service, storage_service)

def test_optimize_success(optimization_service):
    electrolyzer_config = ElectrolyzerConfig(
        electrolyzer_id="E1",
        type=ElectrolyzerType.PEM,
        capacity=1000.0,
        efficiency_params={"a": -0.1, "b": 0.25, "c": 0.6}
    )
    storage_config = StorageConfig(
        storage_id="S1",
        max_capacity=100.0
    )
    optimization_service.electrolyzer_service.get_config.return_value = electrolyzer_config
    optimization_service.storage_service.get_config.return_value = storage_config

    optimization_service.optimize = MagicMock(return_value=OptimizationOutput(
        power_schedule=[500.0] * 24,
        hydrogen_produced=[10.0] * 24,
        storage_levels=[50.0] * 24,
        total_cost=600.0
    ))

    input = OptimizationInput(
        electrolyzer_id="E1",
        storage_id="S1",
        electricity_prices=[0.05] * 24,
        hydrogen_demand=[2.0] * 24
    )
    result = optimization_service.optimize(input)
    assert len(result.power_schedule) == 24
    assert len(result.hydrogen_produced) == 24
    assert len(result.storage_levels) == 24
    assert isinstance(result.total_cost, float)

def test_optimize_missing_electrolyzer(optimization_service):
    optimization_service.electrolyzer_service.get_config.side_effect = ValueError("Electrolyzer ID not found")
    input = OptimizationInput(
        electrolyzer_id="E999",
        storage_id="S1"
    )
    with pytest.raises(ValueError, match="Electrolyzer ID not found"):
        optimization_service.optimize(input)

def test_optimize_missing_storage(optimization_service):
    optimization_service.storage_service.get_config.side_effect = ValueError("Storage ID not found")
    input = OptimizationInput(
        electrolyzer_id="E1",
        storage_id="S999"
    )
    with pytest.raises(ValueError, match="Storage ID not found"):
        optimization_service.optimize(input)