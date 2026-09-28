from pydantic import BaseModel


class Vehicle(BaseModel):
    vehicle_number: int
    longitude: float
    latitude: float
    trip_id: int | None
    vehicle_trip_id: int


class VehiclesResponse(BaseModel):
    vehicles: list[Vehicle]
