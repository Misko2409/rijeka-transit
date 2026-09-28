from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.api.dependencies import get_stop_service
from backend.app.models.api.stop import StopsResponse
from backend.app.services.stop_service import StopService

router = APIRouter(prefix="/stops", tags=["stops"])

StopServiceDependency = Annotated[
    StopService,
    Depends(get_stop_service),
]


@router.get("", response_model=StopsResponse)
async def get_stops(
    service: StopServiceDependency,
) -> StopsResponse:
    return await service.get_stops()
