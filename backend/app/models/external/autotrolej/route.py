from pydantic import BaseModel, Field


class AutotrolejRoute(BaseModel):
    id: int
    broj_linije: str = Field(alias="brojLinije")
    smjer_id: int = Field(alias="smjerId")
    smjer_naziv: str = Field(alias="smjerNaziv")
    varijanta_id: int = Field(alias="varijantaId")
    naziv: str


class AutotrolejRoutesResponse(BaseModel):
    msg: str
    res: dict[str, AutotrolejRoute]
    err: bool
