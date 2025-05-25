"""Modele danych dla ocen w systemie USOS-like."""

import datetime
from pydantic import BaseModel, Field

class OcenaBazowa(BaseModel):
    """Model bazowy dla danych oceny."""
    studentId: str
    grupaId: str
    wystawionePrzez: str
    wartoscOceny: str

class OcenaTworzenie(OcenaBazowa):
    """Model danych do tworzenia nowej oceny."""
    pass

class Ocena(OcenaBazowa):
    """Model danych reprezentujący istniejącą ocenę."""
    ocenaId: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
