import asyncio

import httpx

from backend.app.clients.autotrolej import AutotrolejClient
from backend.app.core.config import get_settings
from backend.app.db.session import SessionLocal
from backend.app.services.vehicle_position import VehiclePositionService


async def main() -> None:
    settings = get_settings()

    async with httpx.AsyncClient(
        base_url="https://api.autotrolej.hr/api/open/v1",
        timeout=10.0,
    ) as http_client:
        autotrolej_client = AutotrolejClient(
            settings=settings,
            http_client=http_client,
        )

        service = VehiclePositionService(
            autotrolej_client=autotrolej_client,
            session_factory=SessionLocal,
        )

        inserted_count = await service.collect_snapshot()

        print(f"Stored {inserted_count} vehicle positions.")


if __name__ == "__main__":
    asyncio.run(main())
