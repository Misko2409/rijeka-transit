from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.api.dependencies import (
    get_departure_service,
    get_stop_service,
)
from backend.app.models.api.departure import DeparturesResponse
from backend.app.models.api.stop import StopsResponse
from backend.app.services.departure_service import DepartureService
from backend.app.services.stop_service import StopService

router = APIRouter(prefix="/stops", tags=["stops"])

StopServiceDependency = Annotated[
    StopService,
    Depends(get_stop_service),
]

DepartureServiceDependency = Annotated[
    DepartureService,
    Depends(get_departure_service),
]


@router.get("", response_model=StopsResponse)
async def get_stops(
    service: StopServiceDependency,
) -> StopsResponse:
    return await service.get_stops()


@router.get(
    "/{stop_id}/departures",
    response_model=DeparturesResponse,
)
async def get_stop_departures(
    stop_id: int,
    service: DepartureServiceDependency,
) -> DeparturesResponse:
    return await service.get_stop_departures(stop_id)
