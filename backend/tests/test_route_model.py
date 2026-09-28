from backend.app.models.api.route import Route, RoutesResponse
from backend.app.models.external.autotrolej.route import (
    AutotrolejRoute,
    AutotrolejRoutesResponse,
)


def test_autotrolej_route_parses_external_response():
    data = {
        "id": 3281,
        "brojLinije": "26",
        "smjerId": 2,
        "smjerNaziv": "B",
        "varijantaId": 11,
        "naziv": "HRELJIN - KRASICA - RIJEKA",
        "polazakList": [],
    }

    route = AutotrolejRoute.model_validate(data)

    assert route.id == 3281
    assert route.broj_linije == "26"
    assert route.smjer_id == 2
    assert route.smjer_naziv == "B"
    assert route.varijanta_id == 11
    assert route.naziv == "HRELJIN - KRASICA - RIJEKA"


def test_autotrolej_routes_response_parses_external_response():
    data = {
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

    response = AutotrolejRoutesResponse.model_validate(data)

    assert response.msg == "ok"
    assert response.err is False
    assert len(response.res) == 1
    assert isinstance(response.res["3281-2-11"], AutotrolejRoute)


def test_route_api_model():
    route = Route(
        unique_id="3281-2-11",
        route_id=3281,
        route_number="26",
        direction_id=2,
        direction="B",
        variant_id=11,
        name="HRELJIN - KRASICA - RIJEKA",
    )

    response = RoutesResponse(routes=[route])

    assert len(response.routes) == 1
    assert response.routes[0].unique_id == "3281-2-11"
    assert response.routes[0].route_number == "26"
    assert response.routes[0].direction == "B"
