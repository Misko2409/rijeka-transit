import httpx

from backend.app.core.config import Settings
from backend.app.models.vehicle import VehiclesResponse


class AutotrolejClient:
    def __init__(
        self,
        settings: Settings,
        http_client: httpx.AsyncClient,
    ) -> None:
        self._settings = settings
        self._http_client = http_client
        self._token: str | None = None

    @property
    def token(self) -> str | None:
        return self._token

    async def login(self) -> str:
        response = await self._http_client.get(
            "/token/login",
            headers={
                "Username": self._settings.autotrolej_username,
                "Password": self._settings.autotrolej_password,
            },
        )

        response.raise_for_status()

        token = response.text.strip()

        if not token:
            raise ValueError("Autotrolej API returned an empty token")

        self._token = token

        return token

    async def get_buses(self) -> VehiclesResponse:
        if not self.token:
            await self.login()

        response = await self._http_client.get(
            "/voznired/autobusi",
            headers={"token": self.token},
        )
        response.raise_for_status()

        return VehiclesResponse.model_validate(response.json())
