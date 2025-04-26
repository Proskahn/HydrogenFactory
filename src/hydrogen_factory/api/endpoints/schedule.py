from fastapi import APIRouter, Depends, HTTPException
from hydrogen_factory.models.schedule import OptimizationInput, OptimizationOutput
from hydrogen_factory.services.optimization_service import OptimizationService
from hydrogen_factory.core.config import get_optimization_service

router = APIRouter()

@router.post("/optimize", response_model=OptimizationOutput)
async def optimize_schedule(
    input: OptimizationInput, 
    service: OptimizationService = Depends(get_optimization_service)
):
    try:
        result = service.optimize(input)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))