from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from backend.app.api.dependencies import get_vehicle_service
from backend.app.main import app
from backend.app.models.api.vehicle import Vehicle, VehiclesResponse

client = TestClient(app)


def test_get_vehicles_returns_vehicles():
    expected_response = VehiclesResponse(
        vehicles=[
            Vehicle(
                vehicle_number=773,
                longitude=14.446925,
                latitude=45.323968,
                trip_id=None,
                vehicle_trip_id=2214313,
            )
        ]
    )

    service = AsyncMock()
    service.get_vehicles.return_value = expected_response

    async def override_get_vehicle_service():
        yield service

    app.dependency_overrides[get_vehicle_service] = override_get_vehicle_service

    try:
        response = client.get("/api/v1/vehicles")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert response.status_code == 200

    data = response.json()

    assert len(data["vehicles"]) == 1

    vehicle = data["vehicles"][0]

    assert vehicle["vehicle_number"] == 773
    assert vehicle["longitude"] == 14.446925
    assert vehicle["latitude"] == 45.323968
    assert vehicle["trip_id"] is None
    assert vehicle["vehicle_trip_id"] == 2214313

    service.get_vehicles.assert_awaited_once()
