from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.api.dependencies import get_route_service
from backend.app.models.api.route import RoutesResponse
from backend.app.services.route_service import RouteService

router = APIRouter(prefix="/routes", tags=["routes"])

RouteServiceDependency = Annotated[
    RouteService,
    Depends(get_route_service),
]


@router.get("", response_model=RoutesResponse)
async def get_routes(
    service: RouteServiceDependency,
) -> RoutesResponse:
    return await service.get_routes()
