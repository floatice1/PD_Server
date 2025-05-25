"""Modele danych dla grup w systemie USOS-like."""

from typing import Optional, List

from pydantic import BaseModel

class GrupaBazowa(BaseModel):
    """Model bazowy dla danych grupy."""
    nazwa: str
    przedmiotId: str
    wykladowcaId: str | None = None

class GrupaTworzenie(GrupaBazowa):
    """Model danych do tworzenia nowej grupy."""
    pass

class Grupa(GrupaBazowa):
    """Model danych reprezentujący istniejącą grupę."""
    grupaId: str
    studenciIds: List[str] = []

class PrzypiszStudentaDoGrupy(BaseModel):
    """Model danych do przypisywania studenta do grupy."""
    studentId: str

class PrzypiszWykladowceDoGrupy(BaseModel):
    """Model danych do przypisywania wykładowcy do grupy."""
    wykladowcaId: str

class GrupaAktualizacja(BaseModel):
    """Model danych do aktualizacji istniejącej grupy."""
    nazwa: Optional[str] = None
    przedmiotId: Optional[str] = None
    wykladowcaId: Optional[str] = None
