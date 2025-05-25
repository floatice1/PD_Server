"""Moduł serwisowy dla zarządzania przedmiotami."""

from typing import List, Optional, Dict, Any
from app.modele.przedmiot import Przedmiot, PrzedmiotTworzenie
from app.repozytoria.przedmiot import RepozytoriumPrzedmiotow

class SerwisPrzedmiotow:
    """Klasa serwisowa do obsługi operacji na przedmiotach."""

    @staticmethod
    async def utworz_przedmiot(dane_przedmiotu: PrzedmiotTworzenie) -> Przedmiot:
        """Tworzy nowy przedmiot."""
        return await RepozytoriumPrzedmiotow.utworz_przedmiot(dane_przedmiotu)

    @staticmethod
    async def pobierz_przedmiot_po_id(przedmiot_id: str) -> Optional[Dict[str, Any]]:
        """Pobiera przedmiot po jego identyfikatorze."""
        return await RepozytoriumPrzedmiotow.pobierz_przedmiot_po_id(przedmiot_id)

    @staticmethod
    async def pobierz_wszystkie_przedmioty() -> List[Dict[str, Any]]:
        """Pobiera listę wszystkich przedmiotów."""
        return await RepozytoriumPrzedmiotow.pobierz_wszystkie_przedmioty()

    @staticmethod
    async def aktualizuj_przedmiot(
        przedmiot_id: str,
        dane_aktualizacji: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Aktualizuje dane istniejącego przedmiotu."""
        if not dane_aktualizacji:
            raise ValueError("Nie podano danych do aktualizacji")

        zaktualizowano = await RepozytoriumPrzedmiotow.aktualizuj_przedmiot(
            przedmiot_id,
            dane_aktualizacji
        )
        if zaktualizowano:
            return await RepozytoriumPrzedmiotow.pobierz_przedmiot_po_id(przedmiot_id)
        return None

    @staticmethod
    async def usun_przedmiot(przedmiot_id: str) -> bool:
        """Usuwa przedmiot po jego identyfikatorze."""
        return await RepozytoriumPrzedmiotow.usun_przedmiot(przedmiot_id)
