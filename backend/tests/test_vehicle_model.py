from backend.app.models.api.vehicle import Vehicle, VehiclesResponse
from backend.app.models.external.autotrolej.vehicle import (
    AutotrolejVehicle,
    AutotrolejVehiclesResponse,
)


def test_autotrolej_vehicle_parses_external_response():
    data = {
        "gbr": 773,
        "lon": 14.446925,
        "lat": 45.323968,
        "voznjaId": None,
        "voznjaBusId": 2214313,
    }

    vehicle = AutotrolejVehicle.model_validate(data)

    assert vehicle.gbr == 773
    assert vehicle.lon == 14.446925
    assert vehicle.lat == 45.323968
    assert vehicle.voznja_id is None
    assert vehicle.voznja_bus_id == 2214313


def test_autotrolej_vehicles_response_parses_external_response():
    data = {
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

    response = AutotrolejVehiclesResponse.model_validate(data)

    assert response.msg == "ok"
    assert response.err is False
    assert len(response.res) == 1
    assert isinstance(response.res[0], AutotrolejVehicle)


def test_vehicle_api_model():
    vehicle = Vehicle(
        vehicle_number=773,
        longitude=14.446925,
        latitude=45.323968,
        trip_id=None,
        vehicle_trip_id=2214313,
    )

    response = VehiclesResponse(vehicles=[vehicle])

    assert len(response.vehicles) == 1
    assert response.vehicles[0].vehicle_number == 773
    assert response.vehicles[0].longitude == 14.446925
    assert response.vehicles[0].latitude == 45.323968
