"""Moduł serwisowy dla zarządzania grupami."""

from typing import List, Optional, Dict, Any
from app.modele.grupa import Grupa, GrupaTworzenie
from app.repozytoria.grupa_rep import RepozytoriumGrup


class SerwisGrup:
    """Klasa serwisowa do obsługi operacji na grupach."""

    @staticmethod
    async def utworz_grupe(dane_grupy: GrupaTworzenie) -> Grupa:
        """Tworzy nową grupę."""
        return await RepozytoriumGrup.utworz_grupe(dane_grupy)

    @staticmethod
    async def pobierz_grupe_po_id(grupa_id: str) -> Optional[Dict[str, Any]]:
        """Pobiera grupę po jej identyfikatorze."""
        return await RepozytoriumGrup.pobierz_grupe_po_id(grupa_id)

    @staticmethod
    async def pobierz_wszystkie_grupy() -> List[Dict[str, Any]]:
        """Pobiera listę wszystkich grup."""
        return await RepozytoriumGrup.pobierz_wszystkie_grupy()

    @staticmethod
    async def aktualizuj_grupe(
        grupa_id: str,
        dane_aktualizacji: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Aktualizuje dane istniejącej grupy."""
        if not dane_aktualizacji:
            raise ValueError("Nie podano danych do aktualizacji")

        zaktualizowano = await RepozytoriumGrup.aktualizuj_grupe(grupa_id, dane_aktualizacji)
        if zaktualizowano:
            return await RepozytoriumGrup.pobierz_grupe_po_id(grupa_id)
        return None

    @staticmethod
    async def usun_grupe(grupa_id: str) -> bool:
        """Usuwa grupę po jej identyfikatorze."""
        return await RepozytoriumGrup.usun_grupe(grupa_id)

    @staticmethod
    async def przypisz_studenta_do_grupy(grupa_id: str, student_id: str) -> bool:
        """Przypisuje studenta do grupy."""
        return await RepozytoriumGrup.przypisz_studenta_do_grupy(grupa_id, student_id)

    @staticmethod
    async def usun_studenta_z_grupy(grupa_id: str, student_id: str) -> bool:
        """Usuwa studenta z grupy."""
        return await RepozytoriumGrup.usun_studenta_z_grupy(grupa_id, student_id)

    @staticmethod
    async def zmien_wykladowce_grupy(grupa_id: str, wykladowca_id: str) -> bool:
        """Zmienia wykładowcę przypisanego do grupy."""
        return await RepozytoriumGrup.zmien_wykladowce_grupy(grupa_id, wykladowca_id)
