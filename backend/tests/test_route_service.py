import asyncio
from unittest.mock import AsyncMock

from backend.app.models.external.autotrolej.route import (
    AutotrolejRoutesResponse,
)
from backend.app.services.route_service import RouteService


def test_get_routes_transforms_autotrolej_data():
    autotrolej_response = AutotrolejRoutesResponse.model_validate(
        {
            "msg": "ok",
            "res": {
                "3281-2-11": {
                    "id": 3281,
                    "brojLinije": "26",
                    "smjerId": 2,
                    "smjerNaziv": "B",
                    "varijantaId": 11,
                    "naziv": "HRELJIN - KRASICA - RIJEKA",
                    "polazakList": [],
                }
            },
            "err": False,
        }
    )

    autotrolej_client = AsyncMock()
    autotrolej_client.get_routes.return_value = autotrolej_response

    service = RouteService(autotrolej_client)

    response = asyncio.run(service.get_routes())

    assert len(response.routes) == 1

    route = response.routes[0]

    assert route.unique_id == "3281-2-11"
    assert route.route_id == 3281
    assert route.route_number == "26"
    assert route.direction_id == 2
    assert route.direction == "B"
    assert route.variant_id == 11
    assert route.name == "HRELJIN - KRASICA - RIJEKA"

    autotrolej_client.get_routes.assert_awaited_once()
