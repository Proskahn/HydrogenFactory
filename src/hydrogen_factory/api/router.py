from fastapi import APIRouter
from hydrogen_factory.api.endpoints import electrolyzer, storage, schedule

api_router = APIRouter()
api_router.include_router(electrolyzer.router, prefix="/electrolyzer", tags=["Electrolyzer"])
api_router.include_router(storage.router, prefix="/storage", tags=["Storage"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["Schedule"])