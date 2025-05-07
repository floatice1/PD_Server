from typing import List, Optional, Dict, Any
from app.modele.uzytkownik import Uzytkownik, UzytkownikTworzenie
from app.repozytoria.uzytkownik import RepozytoriumUzytkownikow

class SerwisUzytkownikow:
    @staticmethod
    async def utworz_uzytkownika(dane_uzytkownika: UzytkownikTworzenie) -> Uzytkownik:
        return await RepozytoriumUzytkownikow.utworz_uzytkownika(dane_uzytkownika)

    @staticmethod
    async def pobierz_uzytkownika_po_id(user_id: str) -> Optional[Dict[str, Any]]:
        return await RepozytoriumUzytkownikow.pobierz_uzytkownika_po_id(user_id)

    @staticmethod
    async def pobierz_wszystkich_uzytkownikow() -> List[Dict[str, Any]]:
        return await RepozytoriumUzytkownikow.pobierz_wszystkich_uzytkownikow()

    @staticmethod
    async def aktualizuj_uzytkownika(user_id: str, dane_uzytkownika: UzytkownikTworzenie) -> Optional[Uzytkownik]:
        return await RepozytoriumUzytkownikow.aktualizuj_uzytkownika(user_id, dane_uzytkownika)

    @staticmethod
    async def usun_uzytkownika(user_id: str) -> bool:
        return await RepozytoriumUzytkownikow.usun_uzytkownika(user_id)