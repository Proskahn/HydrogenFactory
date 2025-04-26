from pydantic import BaseModel, Field, ConfigDict

class StorageConfig(BaseModel):
    storage_id: str = Field(..., description="Unique identifier for the storage")
    max_capacity: float = Field(..., gt=0, description="Maximum storage capacity (kg)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "storage_id": "S1",
                "max_capacity": 100.0,
            }
        }
    )