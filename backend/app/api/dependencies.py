from collections.abc import AsyncGenerator
from typing import Annotated

import httpx
from fastapi import Depends

from backend.app.clients.autotrolej import AutotrolejClient
from backend.app.core.config import get_settings
from backend.app.services.route_service import RouteService
from backend.app.services.stop_service import StopService
from backend.app.services.vehicle_service import VehicleService


async def get_autotrolej_client() -> AsyncGenerator[AutotrolejClient, None]:
    settings = get_settings()

    async with httpx.AsyncClient(
        base_url="https://api.autotrolej.hr/api/open/v1",
        timeout=10.0,
    ) as http_client:
        yield AutotrolejClient(
            settings=settings,
            http_client=http_client,
        )


AutotrolejClientDependency = Annotated[
    AutotrolejClient,
    Depends(get_autotrolej_client),
]


async def get_vehicle_service(
    client: AutotrolejClientDependency,
) -> VehicleService:
    return VehicleService(client)


async def get_stop_service(
    client: AutotrolejClientDependency,
) -> StopService:
    return StopService(client)


async def get_route_service(
    client: AutotrolejClientDependency,
) -> RouteService:
    return RouteService(client)
