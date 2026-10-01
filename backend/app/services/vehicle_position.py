from collections.abc import Callable
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from backend.app.clients.autotrolej import AutotrolejClient
from backend.app.models.external.autotrolej.vehicle import AutotrolejVehicle
from backend.app.repositories.vehicle_position import VehiclePositionRepository


class VehiclePositionService:
    def __init__(
        self,
        autotrolej_client: AutotrolejClient,
        session_factory: Callable[[], Session],
    ) -> None:
        self._autotrolej_client = autotrolej_client
        self._session_factory = session_factory

    async def collect_snapshot(self) -> int:
        response = await self._autotrolej_client.get_buses()
        recorded_at = datetime.now(UTC)

        return self._store_snapshot(
            vehicles=response.res,
            recorded_at=recorded_at,
        )

    def _store_snapshot(
        self,
        vehicles: list[AutotrolejVehicle],
        recorded_at: datetime,
    ) -> int:
        with self._session_factory() as session:
            repository = VehiclePositionRepository(session)

            try:
                inserted_count = repository.add_snapshot(
                    vehicles=vehicles,
                    recorded_at=recorded_at,
                )

                session.commit()

                return inserted_count
            except Exception:
                session.rollback()
                raise
