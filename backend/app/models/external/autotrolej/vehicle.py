from pydantic import BaseModel, Field


class AutotrolejVehicle(BaseModel):
    gbr: int
    lon: float
    lat: float
    voznja_id: int | None = Field(alias="voznjaId")
    voznja_bus_id: int = Field(alias="voznjaBusId")


class AutotrolejVehiclesResponse(BaseModel):
    msg: str
    res: list[AutotrolejVehicle]
    err: bool
