from pydantic import BaseModel

class PrzedmiotBazowy(BaseModel):
    nazwa: str
    opis: str | None = None

class PrzedmiotTworzenie(PrzedmiotBazowy):
    pass

class Przedmiot(PrzedmiotBazowy):
    przedmiotId: str