import asyncio
import logging

from backend.app.services.vehicle_position import VehiclePositionService

logger = logging.getLogger(__name__)


class VehiclePositionCollector:
    def __init__(
        self,
        service: VehiclePositionService,
        interval_seconds: float = 15.0,
    ) -> None:
        self._service = service
        self._interval_seconds = interval_seconds

    async def run(self) -> None:
        logger.info(
            "Vehicle position collector started with %.1f second interval",
            self._interval_seconds,
        )

        try:
            while True:
                try:
                    inserted_count = await self._service.collect_snapshot()

                    logger.info(
                        "Stored vehicle position snapshot with %d positions",
                        inserted_count,
                    )
                except Exception:
                    logger.exception("Failed to collect vehicle position snapshot")

                await asyncio.sleep(self._interval_seconds)

        except asyncio.CancelledError:
            logger.info("Vehicle position collector stopped")
            raise
