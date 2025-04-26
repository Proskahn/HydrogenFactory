from pydantic import BaseModel, Field, ConfigDict
import random

class OptimizationInput(BaseModel):
    electrolyzer_id: str = Field(..., description="ID of the electrolyzer to use")
    storage_id: str = Field(..., description="ID of the storage to use")
    electricity_prices: list[float] = Field(
        default_factory=lambda: [round(random.uniform(0.03, 0.10), 3) for _ in range(24)],
        min_length=24,
        max_length=24,
        description="Hourly electricity prices (€/kWh), randomly generated between 0.03 and 0.10"
    )
    hydrogen_demand: list[float] = Field(
        default_factory=lambda: [round(random.uniform(1.0, 5.0), 2) for _ in range(24)],
        min_length=24,
        max_length=24,
        description="Hourly hydrogen demand (kg), randomly generated between 1.0 and 5.0"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "electrolyzer_id": "E1",
                "storage_id": "S1",
                "electricity_prices": [0.05] * 24,
                "hydrogen_demand": [2.0] * 24,
            }
        }
    )

class OptimizationOutput(BaseModel):
    power_schedule: list[float] = Field(..., description="Hourly power input to electrolyzer (kW)")
    hydrogen_produced: list[float] = Field(..., description="Hourly hydrogen production (kg)")
    storage_levels: list[float] = Field(..., description="Hourly storage levels (kg)")
    total_cost: float = Field(..., description="Total electricity cost (€)")