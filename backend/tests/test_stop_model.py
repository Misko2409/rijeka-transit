from backend.app.models.api.stop import Stop, StopsResponse
from backend.app.models.external.autotrolej.stop import (
    AutotrolejStop,
    AutotrolejStopsResponse,
)


def test_autotrolej_stop_parses_external_response():
    data = {
        "id": 1734,
        "naziv": "i. maja",
        "nazivKratki": "i. maja",
        "gpsX": 14.43316,
        "gpsY": 45.333713,
        "smjer": "B",
        "smjerId": 2,
        "stanicaIdSuprotniSmjer": 1735,
        "polazakList": [],
    }

    stop = AutotrolejStop.model_validate(data)

    assert stop.id == 1734
    assert stop.naziv == "i. maja"
    assert stop.naziv_kratki == "i. maja"
    assert stop.gps_x == 14.43316
    assert stop.gps_y == 45.333713
    assert stop.smjer == "B"
    assert stop.smjer_id == 2
    assert stop.stanica_id_suprotni_smjer == 1735


def test_autotrolej_stops_response_parses_external_response():
    data = {
        "msg": "ok",
        "res": {
            "1734": {
                "id": 1734,
                "naziv": "i. maja",
                "nazivKratki": "i. maja",
                "gpsX": 14.43316,
                "gpsY": 45.333713,
                "smjer": "B",
                "smjerId": 2,
                "stanicaIdSuprotniSmjer": 1735,
            }
        },
        "err": False,
    }

    response = AutotrolejStopsResponse.model_validate(data)

    assert response.msg == "ok"
    assert response.err is False
    assert len(response.res) == 1
    assert isinstance(response.res["1734"], AutotrolejStop)


def test_stop_api_model():
    stop = Stop(
        id=1734,
        name="i. maja",
        short_name="i. maja",
        longitude=14.43316,
        latitude=45.333713,
        direction="B",
        direction_id=2,
        opposite_stop_id=1735,
    )

    response = StopsResponse(stops=[stop])

    assert len(response.stops) == 1
    assert response.stops[0].id == 1734
    assert response.stops[0].name == "i. maja"
    assert response.stops[0].longitude == 14.43316
    assert response.stops[0].latitude == 45.333713
