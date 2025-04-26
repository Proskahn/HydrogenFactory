from enum import Enum
from pydantic import BaseModel, Field

class PowerSupplyType(str, Enum):
    PHOTOVOLTAIC = "PHOTOVOLTAIC"
    WIND = "WIND"
    GRID = "GRID"

class PowerSupplyConfig(BaseModel):
    supply_id: str = Field(..., description="Unique identifier for the power supply")
    type: PowerSupplyType = Field(..., description="Type of power supply")
    capacity: float = Field(..., gt=0, description="Maximum power capacity (kW)")
    availability: list[float] = Field(
        ..., min_items=24, max_items=24, description="Hourly availability (0 to 1) for 24 hours"
    )

    class Config:
        schema_extra = {
            "example": {
                "supply_id": "S1",
                "type": "PHOTOVOLTAIC",
                "capacity": 1500.0,
                "availability": [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3, 0.6, 0.8, 0.9, 1.0, 1.0, 
                                 1.0, 0.9, 0.8, 0.6, 0.3, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            }
        }
