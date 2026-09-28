from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from backend.app.api.dependencies import get_stop_service
from backend.app.main import app
from backend.app.models.api.stop import Stop, StopsResponse

client = TestClient(app)


def test_get_stops_returns_normalized_stops():
    expected_response = StopsResponse(
        stops=[
            Stop(
                id=1734,
                name="i. maja",
                short_name="i. maja",
                longitude=14.43316,
                latitude=45.333713,
                direction="B",
                direction_id=2,
                opposite_stop_id=1735,
            )
        ]
    )

    service = AsyncMock()
    service.get_stops.return_value = expected_response

    async def override_get_stop_service():
        yield service

    app.dependency_overrides[get_stop_service] = override_get_stop_service

    try:
        response = client.get("/api/v1/stops")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert len(data["stops"]) == 1

    stop = data["stops"][0]

    assert stop["id"] == 1734
    assert stop["name"] == "i. maja"
    assert stop["short_name"] == "i. maja"
    assert stop["longitude"] == 14.43316
    assert stop["latitude"] == 45.333713
    assert stop["direction"] == "B"
    assert stop["direction_id"] == 2
    assert stop["opposite_stop_id"] == 1735

    # Our public API must not leak Autotrolej field names.
    assert "naziv" not in stop
    assert "gpsX" not in stop
    assert "gpsY" not in stop

    service.get_stops.assert_awaited_once()
