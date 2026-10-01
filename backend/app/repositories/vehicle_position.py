from datetime import datetime

from geoalchemy2.elements import WKTElement
from sqlalchemy import insert
from sqlalchemy.orm import Session

from backend.app.db.models.vehicle_position import VehiclePosition
from backend.app.models.external.autotrolej.vehicle import AutotrolejVehicle


class VehiclePositionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_snapshot(
        self,
        vehicles: list[AutotrolejVehicle],
        recorded_at: datetime,
    ) -> int:
        if not vehicles:
            return 0

        values = [
            {
                "vehicle_number": vehicle.gbr,
                "trip_id": vehicle.voznja_id,
                "vehicle_trip_id": vehicle.voznja_bus_id,
                "location": WKTElement(
                    f"POINT({vehicle.lon} {vehicle.lat})",
                    srid=4326,
                ),
                "recorded_at": recorded_at,
            }
            for vehicle in vehicles
        ]

        self._session.execute(
            insert(VehiclePosition),
            values,
        )

        return len(values)
