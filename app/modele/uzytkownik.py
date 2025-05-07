from pydantic import BaseModel, EmailStr
from enum import Enum

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