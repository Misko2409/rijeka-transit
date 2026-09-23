import httpx
import pytest

from backend.app.clients.autotrolej import AutotrolejClient
from backend.app.core.config import Settings


@pytest.mark.anyio
async def test_login_stores_and_returns_token():
    expected_token = "test-token"

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/open/v1/token/login"
        assert request.headers["Username"] == "test-user"
        assert request.headers["Password"] == "test-password"

        return httpx.Response(
            status_code=200,
            text=expected_token,
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="https://api.autotrolej.hr/api/open/v1",
    ) as http_client:
        settings = Settings(
            autotrolej_username="test-user",
            autotrolej_password="test-password",
        )

        client = AutotrolejClient(
            settings=settings,
            http_client=http_client,
        )

        token = await client.login()

    assert token == expected_token
    assert client.token == expected_token


@pytest.mark.anyio
async def test_login_raises_error_when_token_is_empty():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            text="",
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="https://api.autotrolej.hr/api/open/v1",
    ) as http_client:
        settings = Settings(
            autotrolej_username="test-user",
            autotrolej_password="test-password",
        )

        client = AutotrolejClient(
            settings=settings,
            http_client=http_client,
        )

        with pytest.raises(
            ValueError,
            match="Autotrolej API returned an empty token",
        ):
            await client.login()

    assert client.token is None


@pytest.mark.anyio
async def test_login_raises_error_on_http_failure():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=401,
            request=request,
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="https://api.autotrolej.hr/api/open/v1",
    ) as http_client:
        settings = Settings(
            autotrolej_username="test-user",
            autotrolej_password="test-password",
        )

        client = AutotrolejClient(
            settings=settings,
            http_client=http_client,
        )

        with pytest.raises(httpx.HTTPStatusError):
            await client.login()

    assert client.token is None


@pytest.mark.anyio
async def test_get_buses_returns_vehicle_data():
    expected_token = "test-token"

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/open/v1/token/login":
            return httpx.Response(
                status_code=200,
                text=expected_token,
            )

        if request.url.path == "/api/open/v1/voznired/autobusi":
            assert request.headers["token"] == expected_token

            return httpx.Response(
                status_code=200,
                json={
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
                },
            )

        raise AssertionError(f"Unexpected request: {request.url}")

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="https://api.autotrolej.hr/api/open/v1",
    ) as http_client:
        settings = Settings(
            autotrolej_username="test-user",
            autotrolej_password="test-password",
        )

        client = AutotrolejClient(
            settings=settings,
            http_client=http_client,
        )

        result = await client.get_buses()

    assert result.msg == "ok"
    assert result.err is False
    assert len(result.res) == 1

    bus = result.res[0]

    assert bus.gbr == 773
    assert bus.lon == 14.446925
    assert bus.lat == 45.323968
    assert bus.voznja_id is None
    assert bus.voznja_bus_id == 2214313
