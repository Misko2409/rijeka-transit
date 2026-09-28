from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from backend.app.api.dependencies import get_route_service
from backend.app.main import app
from backend.app.models.api.route import Route, RoutesResponse

client = TestClient(app)


def test_get_routes_returns_normalized_routes():
    expected_response = RoutesResponse(
        routes=[
            Route(
                unique_id="3281-2-11",
                route_id=3281,
                route_number="26",
                direction_id=2,
                direction="B",
                variant_id=11,
                name="HRELJIN - KRASICA - RIJEKA",
            )
        ]
    )

    service = AsyncMock()
    service.get_routes.return_value = expected_response

    async def override_get_route_service():
        yield service

    app.dependency_overrides[get_route_service] = override_get_route_service

    try:
        response = client.get("/api/v1/routes")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert len(data["routes"]) == 1

    route = data["routes"][0]

    assert route["unique_id"] == "3281-2-11"
    assert route["route_id"] == 3281
    assert route["route_number"] == "26"
    assert route["direction_id"] == 2
    assert route["direction"] == "B"
    assert route["variant_id"] == 11
    assert route["name"] == "HRELJIN - KRASICA - RIJEKA"

    # The public API must not leak Autotrolej field names.
    assert "brojLinije" not in route
    assert "smjerId" not in route
    assert "smjerNaziv" not in route
    assert "varijantaId" not in route
    assert "naziv" not in route
    assert "polazakList" not in route

    service.get_routes.assert_awaited_once()
