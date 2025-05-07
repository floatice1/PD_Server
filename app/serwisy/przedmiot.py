from typing import List, Optional, Dict, Any
from app.modele.przedmiot import Przedmiot, PrzedmiotTworzenie
from app.repozytoria.przedmiot import RepozytoriumPrzedmiotow

class SerwisPrzedmiotow:
    @staticmethod
    async def utworz_przedmiot(dane_przedmiotu: PrzedmiotTworzenie) -> Przedmiot:
        return await RepozytoriumPrzedmiotow.utworz_przedmiot(dane_przedmiotu)

    @staticmethod
    async def pobierz_przedmiot_po_id(przedmiot_id: str) -> Optional[Dict[str, Any]]:
        return await RepozytoriumPrzedmiotow.pobierz_przedmiot_po_id(przedmiot_id)

    @staticmethod
    async def pobierz_wszystkie_przedmioty() -> List[Dict[str, Any]]:
        return await RepozytoriumPrzedmiotow.pobierz_wszystkie_przedmioty()

    @staticmethod
    async def aktualizuj_przedmiot(przedmiot_id: str, dane_przedmiotu: PrzedmiotTworzenie) -> Optional[Przedmiot]:
        return await RepozytoriumPrzedmiotow.aktualizuj_przedmiot(przedmiot_id, dane_przedmiotu)

    @staticmethod
    async def usun_przedmiot(przedmiot_id: str) -> bool:
        return await RepozytoriumPrzedmiotow.usun_przedmiot(przedmiot_id)
