"""Modele danych dla użytkowników w systemie USOS-like."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr

class Rola(str, Enum):
    """Definiuje możliwe role użytkowników."""
    STUDENT = "student"
    WYKLADOWCA = "wykladowca"
    DZIEKANAT = "dziekanat"

class UzytkownikBazowy(BaseModel):
    """Model bazowy dla danych użytkownika."""
    email: EmailStr
    imie: str
    rola: Rola

class UzytkownikTworzenie(UzytkownikBazowy):
    """Model danych do tworzenia nowego użytkownika."""
    haslo: str

class Uzytkownik(UzytkownikBazowy):
    """Model danych reprezentujący istniejącego użytkownika."""
    uid: str

class UzytkownikAktualizacja(BaseModel):
    """Model danych do aktualizacji istniejącego użytkownika."""
    email: Optional[EmailStr] = None
    haslo: Optional[str] = None
    imie: Optional[str] = None
    rola: Optional[Rola] = None

class UzytkownikLogin(BaseModel):
    """Model danych do logowania użytkownika."""
    email: EmailStr
    haslo: str

class UzytkownikInfo(BaseModel):
    """Model danych do pobierania informacji o użytkowniku."""
    uid: str
    email: str
    name: str
    role: str
