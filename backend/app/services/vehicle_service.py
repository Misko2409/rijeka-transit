from backend.app.clients.autotrolej import AutotrolejClient
from backend.app.models.vehicle import VehiclesResponse


class VehicleService:
    def __init__(self, autotrolej_client: AutotrolejClient):
        self._autotrolej_client = autotrolej_client

    async def get_vehicles(self) -> VehiclesResponse:
        return await self._autotrolej_client.get_buses()
