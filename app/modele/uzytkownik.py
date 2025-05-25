from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr

class Rola(str, Enum):
    student = "student"
    wykladowca = "wykladowca"
    dziekanat = "dziekanat"

class UzytkownikBazowy(BaseModel):
    email: EmailStr
    imie: str
    rola: Rola

class UzytkownikTworzenie(UzytkownikBazowy):
    haslo: str

class Uzytkownik(UzytkownikBazowy):
    uid: str

class UzytkownikAktualizacja(BaseModel):
    email: Optional[EmailStr] = None
    haslo: Optional[str] = None
    imie: Optional[str] = None
    rola: Optional[Rola] = None

class UzytkownikLogin(BaseModel):
    email: EmailStr
    haslo: str
