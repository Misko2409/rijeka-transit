from pydantic import BaseModel, Field


class Vehicle(BaseModel):
    gbr: int
    lon: float
    lat: float
    voznja_id: int | None = Field(alias="voznjaId")
    voznja_bus_id: int = Field(alias="voznjaBusId")


class VehiclesResponse(BaseModel):
    msg: str
    res: list[Vehicle]
    err: bool
