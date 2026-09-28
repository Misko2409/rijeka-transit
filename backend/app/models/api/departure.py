from datetime import datetime

from pydantic import BaseModel


class Departure(BaseModel):
    stop_id: int
    trip_id: int
    vehicle_trip_id: int
    trip_stop_id: int
    route_id: int
    route_unique_id: str
    departure_time: datetime
    arrival_time: datetime


class DeparturesResponse(BaseModel):
    departures: list[Departure]
