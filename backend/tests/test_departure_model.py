from datetime import datetime

from backend.app.models.api.departure import Departure, DeparturesResponse
from backend.app.models.external.autotrolej.departure import (
    AutotrolejDeparture,
    AutotrolejStopDeparturesResponse,
)


def test_autotrolej_departure_parses_external_response():
    data = {
        "stanicaId": 1734,
        "voznjaId": 1433735,
        "voznjaBusId": 0,
        "voznjaStanicaId": 25804783,
        "linijaId": 2132,
        "uniqueLinijaId": "2132-2-0",
        "polazak": "2026-09-28T05:19:00",
        "dolazak": "2026-09-28T05:19:00",
    }

    departure = AutotrolejDeparture.model_validate(data)

    assert departure.stanica_id == 1734
    assert departure.voznja_id == 1433735
    assert departure.voznja_bus_id == 0
    assert departure.voznja_stanica_id == 25804783
    assert departure.linija_id == 2132
    assert departure.unique_linija_id == "2132-2-0"

    expected_time = datetime.fromisoformat("2026-09-28T05:19:00")

    assert departure.polazak == expected_time
    assert departure.dolazak == expected_time


def test_stop_departures_response_parses_external_response():
    data = {
        "msg": "ok",
        "res": {
            "id": 1734,
            "naziv": "i. maja",
            "nazivKratki": "i. maja",
            "gpsX": 14.43316,
            "gpsY": 45.333713,
            "smjer": "B",
            "smjerId": 2,
            "stanicaIdSuprotniSmjer": 1735,
            "polazakList": [
                {
                    "stanicaId": 1734,
                    "voznjaId": 1433735,
                    "voznjaBusId": 0,
                    "voznjaStanicaId": 25804783,
                    "linijaId": 2132,
                    "uniqueLinijaId": "2132-2-0",
                    "polazak": "2026-09-28T05:19:00",
                    "dolazak": "2026-09-28T05:19:00",
                }
            ],
        },
        "err": False,
    }

    response = AutotrolejStopDeparturesResponse.model_validate(data)

    assert response.msg == "ok"
    assert response.err is False
    assert response.res.id == 1734
    assert len(response.res.polazak_list) == 1


def test_departure_api_model():
    departure = Departure(
        stop_id=1734,
        trip_id=1433735,
        vehicle_trip_id=0,
        trip_stop_id=25804783,
        route_id=2132,
        route_unique_id="2132-2-0",
        departure_time=datetime.fromisoformat("2026-09-28T05:19:00"),
        arrival_time=datetime.fromisoformat("2026-09-28T05:19:00"),
    )

    response = DeparturesResponse(departures=[departure])

    assert len(response.departures) == 1
    assert response.departures[0].stop_id == 1734
    assert response.departures[0].route_unique_id == "2132-2-0"
