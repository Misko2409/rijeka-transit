from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.api.dependencies import (
    get_departure_service,
    get_route_service,
)
from backend.app.models.api.departure import DeparturesResponse
from backend.app.models.api.route import RoutesResponse
from backend.app.services.departure_service import DepartureService
from backend.app.services.route_service import RouteService

router = APIRouter(prefix="/routes", tags=["routes"])

RouteServiceDependency = Annotated[
    RouteService,
    Depends(get_route_service),
]

DepartureServiceDependency = Annotated[
    DepartureService,
    Depends(get_departure_service),
]


@router.get("", response_model=RoutesResponse)
async def get_routes(
    service: RouteServiceDependency,
) -> RoutesResponse:
    return await service.get_routes()


@router.get(
    "/{route_unique_id}/departures",
    response_model=DeparturesResponse,
)
async def get_route_departures(
    route_unique_id: str,
    service: DepartureServiceDependency,
) -> DeparturesResponse:
    return await service.get_route_departures(route_unique_id)
