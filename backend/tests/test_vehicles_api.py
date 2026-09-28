from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from backend.app.api.dependencies import get_vehicle_service
from backend.app.main import app
from backend.app.models.vehicle import VehiclesResponse

client = TestClient(app)


def test_get_vehicles_returns_vehicles():
    expected_response = VehiclesResponse.model_validate(
        {
            "msg": "ok",
            "res": [
                {
                    "gbr": 773,
                    "lon": 14.446925,
                    "lat": 45.323968,
                    "voznjaId": None,
                    "voznjaBusId": 2214313,
                }
            ],
            "err": False,
        }
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

    assert data["msg"] == "ok"
    assert data["err"] is False
    assert len(data["res"]) == 1
    assert data["res"][0]["gbr"] == 773

    service.get_vehicles.assert_awaited_once()
