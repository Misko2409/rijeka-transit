from backend.app.clients.autotrolej import AutotrolejClient
from backend.app.models.api.stop import Stop, StopsResponse


class StopService:
    def __init__(self, autotrolej_client: AutotrolejClient) -> None:
        self._autotrolej_client = autotrolej_client

    async def get_stops(self) -> StopsResponse:
        response = await self._autotrolej_client.get_stops()

        stops = [
            Stop(
                id=stop.id,
                name=stop.naziv,
                short_name=stop.naziv_kratki,
                longitude=stop.gps_x,
                latitude=stop.gps_y,
                direction=stop.smjer,
                direction_id=stop.smjer_id,
                opposite_stop_id=stop.stanica_id_suprotni_smjer,
            )
            for stop in response.res.values()
        ]

        return StopsResponse(stops=stops)
