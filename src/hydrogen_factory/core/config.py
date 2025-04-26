from fastapi import Depends
from hydrogen_factory.services.electrolyzer_service import ElectrolyzerService
from hydrogen_factory.services.storage_service import StorageService
from hydrogen_factory.services.optimization_service import OptimizationService

_electrolyzer_service = ElectrolyzerService()
_storage_service = StorageService()
_optimization_service = OptimizationService(_electrolyzer_service, _storage_service)

def get_electrolyzer_service() -> ElectrolyzerService:
    return _electrolyzer_service

def get_storage_service() -> StorageService:
    return _storage_service

def get_optimization_service() -> OptimizationService:
    return _optimization_service