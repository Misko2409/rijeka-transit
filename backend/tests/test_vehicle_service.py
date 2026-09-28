import asyncio
from unittest.mock import AsyncMock

from backend.app.models.external.autotrolej.vehicle import (
    AutotrolejVehiclesResponse,
)
from backend.app.services.vehicle_service import VehicleService


def test_get_vehicles_transforms_autotrolej_data():
    autotrolej_response = AutotrolejVehiclesResponse.model_validate(
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

    autotrolej_client = AsyncMock()
    autotrolej_client.get_buses.return_value = autotrolej_response

    service = VehicleService(autotrolej_client)

    response = asyncio.run(service.get_vehicles())

    assert len(response.vehicles) == 1

    vehicle = response.vehicles[0]

    assert vehicle.vehicle_number == 773
    assert vehicle.longitude == 14.446925
    assert vehicle.latitude == 45.323968
    assert vehicle.trip_id is None
    assert vehicle.vehicle_trip_id == 2214313

    autotrolej_client.get_buses.assert_awaited_once()
