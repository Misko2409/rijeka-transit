from datetime import datetime
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from backend.app.api.dependencies import get_departure_service
from backend.app.main import app
from backend.app.models.api.departure import Departure, DeparturesResponse

client = TestClient(app)


def create_departures_response() -> DeparturesResponse:
    return DeparturesResponse(
        departures=[
            Departure(
                stop_id=1734,
                trip_id=1433735,
                vehicle_trip_id=0,
                trip_stop_id=25804783,
                route_id=2132,
                route_unique_id="2132-2-0",
                departure_time=datetime.fromisoformat("2026-09-28T05:19:00"),
                arrival_time=datetime.fromisoformat("2026-09-28T05:19:00"),
            )
        ]
    )


def test_get_stop_departures_returns_normalized_departures():
    service = AsyncMock()
    service.get_stop_departures.return_value = create_departures_response()

    app.dependency_overrides[get_departure_service] = lambda: service

    try:
        response = client.get("/api/v1/stops/1734/departures")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()
    assert len(data["departures"]) == 1

    departure = data["departures"][0]

    assert departure["stop_id"] == 1734
    assert departure["route_unique_id"] == "2132-2-0"
    assert departure["departure_time"] == "2026-09-28T05:19:00"

    assert "stanicaId" not in departure
    assert "voznjaId" not in departure
    assert "polazak" not in departure

    service.get_stop_departures.assert_awaited_once_with(1734)


def test_get_route_departures_returns_normalized_departures():
    service = AsyncMock()
    service.get_route_departures.return_value = create_departures_response()

    app.dependency_overrides[get_departure_service] = lambda: service

    try:
        response = client.get("/api/v1/routes/2132-2-0/departures")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()
    assert len(data["departures"]) == 1

    departure = data["departures"][0]

    assert departure["route_id"] == 2132
    assert departure["route_unique_id"] == "2132-2-0"
    assert departure["arrival_time"] == "2026-09-28T05:19:00"

    assert "linijaId" not in departure
    assert "uniqueLinijaId" not in departure
    assert "dolazak" not in departure

    service.get_route_departures.assert_awaited_once_with("2132-2-0")
