from fastapi import APIRouter, Depends, HTTPException
from hydrogen_factory.models.storage import StorageConfig
from hydrogen_factory.services.storage_service import StorageService
from hydrogen_factory.core.config import get_storage_service

router = APIRouter()

@router.post("/configure", response_model=StorageConfig)
async def configure_storage(
    config: StorageConfig, 
    service: StorageService = Depends(get_storage_service)
):
    try:
        service.configure(config)
        return config
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))