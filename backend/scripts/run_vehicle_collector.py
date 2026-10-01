import asyncio
import logging

import httpx

from backend.app.clients.autotrolej import AutotrolejClient
from backend.app.collectors.vehicle_position import VehiclePositionCollector
from backend.app.core.config import get_settings
from backend.app.db.session import SessionLocal
from backend.app.services.vehicle_position import VehiclePositionService


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

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

        collector = VehiclePositionCollector(
            service=service,
            interval_seconds=15.0,
        )

        await collector.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
