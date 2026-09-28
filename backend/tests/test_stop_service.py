import asyncio
from unittest.mock import AsyncMock

from backend.app.models.external.autotrolej.stop import (
    AutotrolejStopsResponse,
)
from backend.app.services.stop_service import StopService


def test_get_stops_transforms_autotrolej_data():
    autotrolej_response = AutotrolejStopsResponse.model_validate(
        {
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
                    "polazakList": [],
                }
            },
            "err": False,
        }
    )

    autotrolej_client = AsyncMock()
    autotrolej_client.get_stops.return_value = autotrolej_response

    service = StopService(autotrolej_client)

    response = asyncio.run(service.get_stops())

    assert len(response.stops) == 1

    stop = response.stops[0]

    assert stop.id == 1734
    assert stop.name == "i. maja"
    assert stop.short_name == "i. maja"
    assert stop.longitude == 14.43316
    assert stop.latitude == 45.333713
    assert stop.direction == "B"
    assert stop.direction_id == 2
    assert stop.opposite_stop_id == 1735

    autotrolej_client.get_stops.assert_awaited_once()
