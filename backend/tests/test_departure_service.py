import asyncio
from unittest.mock import AsyncMock

from backend.app.models.external.autotrolej.departure import (
    AutotrolejRouteDeparturesResponse,
    AutotrolejStopDeparturesResponse,
)
from backend.app.services.departure_service import DepartureService

DEPARTURE = {
    "stanicaId": 1734,
    "voznjaId": 1433735,
    "voznjaBusId": 0,
    "voznjaStanicaId": 25804783,
    "linijaId": 2132,
    "uniqueLinijaId": "2132-2-0",
    "polazak": "2026-09-28T05:19:00",
    "dolazak": "2026-09-28T05:19:00",
}


def test_get_stop_departures_transforms_autotrolej_data():
    autotrolej_response = AutotrolejStopDeparturesResponse.model_validate(
        {
            "msg": "ok",
            "res": {
                "id": 1734,
                "polazakList": [DEPARTURE],
            },
            "err": False,
        }
    )

    autotrolej_client = AsyncMock()
    autotrolej_client.get_stop_departures.return_value = autotrolej_response

    service = DepartureService(autotrolej_client)

    response = asyncio.run(service.get_stop_departures(1734))

    assert len(response.departures) == 1

    departure = response.departures[0]

    assert departure.stop_id == 1734
    assert departure.trip_id == 1433735
    assert departure.vehicle_trip_id == 0
    assert departure.trip_stop_id == 25804783
    assert departure.route_id == 2132
    assert departure.route_unique_id == "2132-2-0"

    autotrolej_client.get_stop_departures.assert_awaited_once_with(1734)


def test_get_route_departures_transforms_autotrolej_data():
    autotrolej_response = AutotrolejRouteDeparturesResponse.model_validate(
        {
            "msg": "ok",
            "res": {
                "id": 2132,
                "polazakList": [DEPARTURE],
            },
            "err": False,
        }
    )

    autotrolej_client = AsyncMock()
    autotrolej_client.get_route_departures.return_value = autotrolej_response

    service = DepartureService(autotrolej_client)

    response = asyncio.run(service.get_route_departures("2132-2-0"))

    assert len(response.departures) == 1

    departure = response.departures[0]

    assert departure.stop_id == 1734
    assert departure.route_id == 2132
    assert departure.route_unique_id == "2132-2-0"

    autotrolej_client.get_route_departures.assert_awaited_once_with("2132-2-0")
