from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.api.dependencies import get_vehicle_service
from backend.app.models.vehicle import VehiclesResponse
from backend.app.services.vehicle_service import VehicleService

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

VehicleServiceDependency = Annotated[
    VehicleService,
    Depends(get_vehicle_service),
]


@router.get("", response_model=VehiclesResponse)
async def get_vehicles(
    service: VehicleServiceDependency,
) -> VehiclesResponse:
    return await service.get_vehicles()
