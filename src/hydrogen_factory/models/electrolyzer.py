from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

class ElectrolyzerType(str, Enum):
    PEM = "PEM"
    ALKALINE = "ALKALINE"

class ElectrolyzerConfig(BaseModel):
    electrolyzer_id: str = Field(..., description="Unique identifier for the electrolyzer")
    type: ElectrolyzerType = Field(..., description="Type of electrolyzer (PEM or ALKALINE)")
    capacity: float = Field(..., gt=0, description="Maximum power capacity (kW)")
    efficiency: float = Field(0.02, gt=0, description="Constant efficiency (kg H₂/kWh)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "electrolyzer_id": "E1",
                "type": "PEM",
                "capacity": 1000.0,
                "efficiency": 0.02,
            }
        }
    )