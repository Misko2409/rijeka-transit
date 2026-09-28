from pydantic import BaseModel


class Route(BaseModel):
    unique_id: str
    route_id: int
    route_number: str
    direction_id: int
    direction: str
    variant_id: int
    name: str


class RoutesResponse(BaseModel):
    routes: list[Route]
