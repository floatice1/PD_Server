"""Modele danych dla przedmiotów w systemie USOS-like."""

from pydantic import BaseModel

class PrzedmiotBazowy(BaseModel):
    """Model bazowy dla danych przedmiotu."""
    nazwa: str
    opis: str

class PrzedmiotTworzenie(PrzedmiotBazowy):
    """Model danych do tworzenia nowego przedmiotu."""
    pass

class Przedmiot(PrzedmiotBazowy):
    """Model danych reprezentujący istniejący przedmiot."""
    przedmiotId: str
