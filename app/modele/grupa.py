from pydantic import BaseModel
from typing import Optional, List

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

class GrupaAktualizacja(BaseModel):
    nazwa: Optional[str] = None
    przedmiotId: Optional[str] = None
    wykladowcaId: Optional[str] = None