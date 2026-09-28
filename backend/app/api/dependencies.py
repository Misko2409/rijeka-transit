from collections.abc import AsyncGenerator

import httpx

from backend.app.clients.autotrolej import AutotrolejClient
from backend.app.core.config import get_settings
from backend.app.services.stop_service import StopService
from backend.app.services.vehicle_service import VehicleService


async def get_vehicle_service() -> AsyncGenerator[VehicleService, None]:
    settings = get_settings()

    async with httpx.AsyncClient(
        base_url="https://api.autotrolej.hr/api/open/v1",
        timeout=10.0,
    ) as http_client:
        client = AutotrolejClient(
            settings=settings,
            http_client=http_client,
        )

        yield VehicleService(client)


async def get_stop_service() -> AsyncGenerator[StopService, None]:
    settings = get_settings()

    async with httpx.AsyncClient(
        base_url="https://api.autotrolej.hr/api/open/v1",
        timeout=10.0,
    ) as http_client:
        client = AutotrolejClient(
            settings=settings,
            http_client=http_client,
        )

        yield StopService(client)
