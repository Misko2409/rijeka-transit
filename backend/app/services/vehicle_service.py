from backend.app.clients.autotrolej import AutotrolejClient
from backend.app.models.api.vehicle import Vehicle, VehiclesResponse


class VehicleService:
    def __init__(self, autotrolej_client: AutotrolejClient) -> None:
        self._autotrolej_client = autotrolej_client

    async def get_vehicles(self) -> VehiclesResponse:
        response = await self._autotrolej_client.get_buses()

        vehicles = [
            Vehicle(
                vehicle_number=vehicle.gbr,
                longitude=vehicle.lon,
                latitude=vehicle.lat,
                trip_id=vehicle.voznja_id,
                vehicle_trip_id=vehicle.voznja_bus_id,
            )
            for vehicle in response.res
        ]

        return VehiclesResponse(vehicles=vehicles)
