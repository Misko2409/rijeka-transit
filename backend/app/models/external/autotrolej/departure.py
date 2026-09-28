from datetime import datetime

from pydantic import BaseModel, Field


class AutotrolejDeparture(BaseModel):
    stanica_id: int = Field(alias="stanicaId")
    voznja_id: int = Field(alias="voznjaId")
    voznja_bus_id: int = Field(alias="voznjaBusId")
    voznja_stanica_id: int = Field(alias="voznjaStanicaId")
    linija_id: int = Field(alias="linijaId")
    unique_linija_id: str = Field(alias="uniqueLinijaId")
    polazak: datetime
    dolazak: datetime


class AutotrolejStopDeparturesResponseData(BaseModel):
    id: int
    polazak_list: list[AutotrolejDeparture] = Field(alias="polazakList")


class AutotrolejStopDeparturesResponse(BaseModel):
    msg: str
    res: AutotrolejStopDeparturesResponseData
    err: bool


class AutotrolejRouteDeparturesResponseData(BaseModel):
    id: int
    polazak_list: list[AutotrolejDeparture] = Field(alias="polazakList")


class AutotrolejRouteDeparturesResponse(BaseModel):
    msg: str
    res: AutotrolejRouteDeparturesResponseData
    err: bool
