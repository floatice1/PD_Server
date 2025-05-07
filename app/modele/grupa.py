from pydantic import BaseModel
from typing import List

class GrupaBazowa(BaseModel):
    nazwa: str
    przedmiotId: str
    wykladowcaId: str | None = None

class GrupaTworzenie(GrupaBazowa):
    pass

class Grupa(GrupaBazowa):
    grupaId: str
    studenciIds: List[str] = []

class PrzypiszStudentaDoGrupy(BaseModel):
    studentId: str

class PrzypiszWykladowceDoGrupy(BaseModel):
    wykladowcaId: str