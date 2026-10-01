from datetime import datetime, timezone
from unittest.mock import MagicMock

from backend.app.models.external.autotrolej.vehicle import AutotrolejVehicle
from backend.app.repositories.vehicle_position import VehiclePositionRepository


def test_add_snapshot_inserts_all_vehicle_positions() -> None:
    session = MagicMock()
    repository = VehiclePositionRepository(session)

    recorded_at = datetime(
        2026,
        10,
        1,
        16,
        0,
        0,
        tzinfo=timezone.utc,
    )

    vehicles = [
        AutotrolejVehicle(
            gbr=773,
            lon=14.446925,
            lat=45.323968,
            voznjaId=None,
            voznjaBusId=2214313,
        ),
        AutotrolejVehicle(
            gbr=811,
            lon=14.451234,
            lat=45.329876,
            voznjaId=1433806,
            voznjaBusId=2214314,
        ),
    ]

    inserted_count = repository.add_snapshot(
        vehicles=vehicles,
        recorded_at=recorded_at,
    )

    assert inserted_count == 2

    session.execute.assert_called_once()

    _, values = session.execute.call_args.args

    assert len(values) == 2

    assert values[0]["vehicle_number"] == 773
    assert values[0]["trip_id"] is None
    assert values[0]["vehicle_trip_id"] == 2214313
    assert values[0]["recorded_at"] == recorded_at

    assert values[1]["vehicle_number"] == 811
    assert values[1]["trip_id"] == 1433806
    assert values[1]["vehicle_trip_id"] == 2214314
    assert values[1]["recorded_at"] == recorded_at

    assert str(values[0]["location"]) == "POINT(14.446925 45.323968)"
    assert str(values[1]["location"]) == "POINT(14.451234 45.329876)"


def test_add_snapshot_with_no_vehicles_does_not_execute_insert() -> None:
    session = MagicMock()
    repository = VehiclePositionRepository(session)

    recorded_at = datetime(
        2026,
        10,
        1,
        16,
        0,
        0,
        tzinfo=timezone.utc,
    )

    inserted_count = repository.add_snapshot(
        vehicles=[],
        recorded_at=recorded_at,
    )

    assert inserted_count == 0
    session.execute.assert_not_called()
