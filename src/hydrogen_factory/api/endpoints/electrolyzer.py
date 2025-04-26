from fastapi import APIRouter, Depends, HTTPException
from hydrogen_factory.models.electrolyzer import ElectrolyzerConfig
from hydrogen_factory.services.electrolyzer_service import ElectrolyzerService
from hydrogen_factory.core.config import get_electrolyzer_service

router = APIRouter()

@router.post("/configure", response_model=ElectrolyzerConfig)
async def configure_electrolyzer(
    config: ElectrolyzerConfig, 
    service: ElectrolyzerService = Depends(get_electrolyzer_service)
):
    try:
        service.configure(config)
        return config
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))