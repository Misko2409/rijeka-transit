from pydantic import BaseModel


class Stop(BaseModel):
    id: int
    name: str
    short_name: str | None
    longitude: float
    latitude: float
    direction: str | None
    direction_id: int | None
    opposite_stop_id: int | None


class StopsResponse(BaseModel):
    stops: list[Stop]
