from backend.app.clients.autotrolej import AutotrolejClient
from backend.app.models.api.departure import Departure, DeparturesResponse
from backend.app.models.external.autotrolej.departure import (
    AutotrolejDeparture,
)


class DepartureService:
    def __init__(self, autotrolej_client: AutotrolejClient) -> None:
        self._autotrolej_client = autotrolej_client

    @staticmethod
    def _transform_departures(
        departures: list[AutotrolejDeparture],
    ) -> DeparturesResponse:
        return DeparturesResponse(
            departures=[
                Departure(
                    stop_id=departure.stanica_id,
                    trip_id=departure.voznja_id,
                    vehicle_trip_id=departure.voznja_bus_id,
                    trip_stop_id=departure.voznja_stanica_id,
                    route_id=departure.linija_id,
                    route_unique_id=departure.unique_linija_id,
                    departure_time=departure.polazak,
                    arrival_time=departure.dolazak,
                )
                for departure in departures
            ]
        )

    async def get_stop_departures(
        self,
        stop_id: int,
    ) -> DeparturesResponse:
        response = await self._autotrolej_client.get_stop_departures(stop_id)

        return self._transform_departures(response.res.polazak_list)

    async def get_route_departures(
        self,
        route_unique_id: str,
    ) -> DeparturesResponse:
        response = await self._autotrolej_client.get_route_departures(route_unique_id)

        return self._transform_departures(response.res.polazak_list)
