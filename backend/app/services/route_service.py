from backend.app.clients.autotrolej import AutotrolejClient
from backend.app.models.api.route import Route, RoutesResponse


class RouteService:
    def __init__(self, autotrolej_client: AutotrolejClient) -> None:
        self._autotrolej_client = autotrolej_client

    async def get_routes(self) -> RoutesResponse:
        response = await self._autotrolej_client.get_routes()

        routes = [
            Route(
                unique_id=unique_id,
                route_id=route.id,
                route_number=route.broj_linije,
                direction_id=route.smjer_id,
                direction=route.smjer_naziv,
                variant_id=route.varijanta_id,
                name=route.naziv,
            )
            for unique_id, route in response.res.items()
        ]

        return RoutesResponse(routes=routes)
