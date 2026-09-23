from backend.app.models.vehicle import Vehicle, VehiclesResponse


def test_vehicle_parses_autotrolej_response():
    data = {
        "gbr": 773,
        "lon": 14.446925,
        "lat": 45.323968,
        "voznjaId": None,
        "voznjaBusId": 2214313,
    }

    vehicle = Vehicle.model_validate(data)

    assert vehicle.gbr == 773
    assert vehicle.lon == 14.446925
    assert vehicle.lat == 45.323968
    assert vehicle.voznja_id is None
    assert vehicle.voznja_bus_id == 2214313


def test_vehicles_response_parses_autotrolej_response():
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

    response = VehiclesResponse.model_validate(data)

    assert response.msg == "ok"
    assert response.err is False
    assert len(response.res) == 1
    assert isinstance(response.res[0], Vehicle)
    assert response.res[0].gbr == 773
