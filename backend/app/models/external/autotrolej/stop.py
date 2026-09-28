from pydantic import BaseModel, Field


class AutotrolejStop(BaseModel):
    id: int
    naziv: str
    naziv_kratki: str | None = Field(alias="nazivKratki")
    gps_x: float = Field(alias="gpsX")
    gps_y: float = Field(alias="gpsY")
    smjer: str | None
    smjer_id: int | None = Field(alias="smjerId")
    stanica_id_suprotni_smjer: int | None = Field(alias="stanicaIdSuprotniSmjer")


class AutotrolejStopsResponse(BaseModel):
    msg: str
    res: dict[str, AutotrolejStop]
    err: bool
